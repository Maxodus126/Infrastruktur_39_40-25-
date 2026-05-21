import json
import boto3
import pytest
import os

# ─────────────────────────────────────────────
# Konfigurasi endpoint LocalStack
# ─────────────────────────────────────────────
ENDPOINT_URL = os.environ.get("DYNAMODB_ENDPOINT", "http://localhost:4566")
REGION       = "us-east-1"
TABLE_NAME   = "mahasiswa"

# ─────────────────────────────────────────────
# (1) Fixture: buat tabel DynamoDB + insert 2 mahasiswa
# ─────────────────────────────────────────────
@pytest.fixture(scope="module")
def dynamodb_table():
    """
    Setup fixture: membuat tabel mahasiswa dan insert 2 data mahasiswa.
    Cleanup dilakukan setelah semua test selesai.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=ENDPOINT_URL,
        region_name=REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    # Coba buat tabel (mungkin sudah ada dari setup CI)
    try:
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "StudentId", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "StudentId", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        table.wait_until_exists()
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        # Tabel sudah ada — pakai yang existing
        table = dynamodb.Table(TABLE_NAME)

    # Insert 2 data mahasiswa
    table.put_item(Item={
        "StudentId": "20230001",
        "Nama":      "Budi Santoso",
        "Jurusan":   "Teknik Informatika",
        "Semester":  5
    })
    table.put_item(Item={
        "StudentId": "20230002",
        "Nama":      "Siti Rahayu",
        "Jurusan":   "Teknik Informatika",
        "Semester":  5
    })

    # Yield tabel ke test
    yield table

    # (3) Cleanup setelah test selesai
    table.delete_item(Key={"StudentId": "20230001"})
    table.delete_item(Key={"StudentId": "20230002"})
    print("\n[teardown] Data test dihapus dari tabel mahasiswa")


# ─────────────────────────────────────────────
# (2) Test: GET /students mengembalikan 200 & data tidak kosong
# ─────────────────────────────────────────────
def test_get_students_returns_200(dynamodb_table):
    """Test bahwa Lambda GET /students mengembalikan statusCode 200"""
    lambda_client = boto3.client(
        "lambda",
        endpoint_url=ENDPOINT_URL,
        region_name=REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    payload = {
        "httpMethod": "GET",
        "path": "/students",
        "queryStringParameters": None
    }

    response = lambda_client.invoke(
        FunctionName="GetStudents",
        Payload=json.dumps(payload).encode()
    )

    result = json.loads(response["Payload"].read())

    assert result["statusCode"] == 200, \
        f"Expected 200, got {result['statusCode']}"

    print(f"\n[PASS] statusCode = {result['statusCode']}")


def test_get_students_data_not_empty(dynamodb_table):
    """Test bahwa GET /students mengembalikan data tidak kosong"""
    lambda_client = boto3.client(
        "lambda",
        endpoint_url=ENDPOINT_URL,
        region_name=REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    payload = {"httpMethod": "GET", "path": "/students"}
    response = lambda_client.invoke(
        FunctionName="GetStudents",
        Payload=json.dumps(payload).encode()
    )

    result   = json.loads(response["Payload"].read())
    body     = json.loads(result["body"])
    students = body.get("students", [])
    count    = body.get("count", 0)

    # Data tidak boleh kosong
    assert len(students) > 0, "students list harus tidak kosong"
    assert count >= 2,        f"Minimal 2 mahasiswa, dapat {count}"

    # Pastikan data yang diinsert ada
    ids = [s["StudentId"] for s in students]
    assert "20230001" in ids, "StudentId 20230001 harus ada"
    assert "20230002" in ids, "StudentId 20230002 harus ada"

    print(f"\n[PASS] Jumlah mahasiswa = {count}")
    for s in students:
        print(f"  - {s['StudentId']} | {s['Nama']} | {s['Jurusan']}")
