# 🖥️ IF1405 — Infrastruktur Cloud dan Sistem Terdistribusi

<div align="center">

![LocalStack](https://img.shields.io/badge/LocalStack-3.8.1-blueviolet?style=for-the-badge&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![pytest](https://img.shields.io/badge/pytest-8.x-green?style=for-the-badge&logo=pytest)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-black?style=for-the-badge&logo=github-actions)
![AWS CLI](https://img.shields.io/badge/AWS_CLI-Local-orange?style=for-the-badge&logo=amazon-aws)
![Docker](https://img.shields.io/badge/Docker-Required-2496ED?style=for-the-badge&logo=docker)

**Praktikum Soal 39 & 40 — LocalStack AWS CLI + GitHub Actions CI/CD**

*UTS Genap Tahun Akademik 2025/2026*

</div>

---

## 👤 Identitas Mahasiswa

| Field | Detail |
|---|---|
| **Nama Mahasiswa** | Aflin Awaludin |
| **NIM** | 24360007 |
| **Program Studi** | Teknik Informatika |
| **Mata Kuliah** | IF1405 — Infrastruktur Cloud dan Sistem Terdistribusi (4 SKS) |
| **Dosen Pengampu** | Dikky Suryadi S.Kom, M.Kom |
| **Kelas** | Hybrid |
| **Hari/Tanggal Ujian** | Rabu, 20 Mei 2026 |
| **Waktu** | 09:00 – 12:00 WIB |
| **Institusi** | Institut Sains dan Teknologi Nasional (ISTN) |

---

## 📁 Struktur Folder Lengkap

```
aflin/
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── 📄 test.yml                  ← [Soal 40a & 40b] GitHub Actions CI/CD workflow
│                                            Trigger  : push ke branch main
│                                            Service  : LocalStack sebagai Docker container
│                                            Env Vars : AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
│                                                       AWS_DEFAULT_REGION, AWS_ENDPOINT_URL
│
├── 📄 handler.py                        ← [Soal 39e] AWS Lambda function Python
│                                            Handler  : lambda_handler(event, context)
│                                            Endpoint : GET /students
│                                            Fungsi   : Scan seluruh item dari DynamoDB tabel 'mahasiswa'
│                                            Fitur    : Pagination otomatis, error handling 500
│
├── 📄 test_lambda.py                    ← [Soal 40c] pytest test suite untuk Lambda GetStudents
│                                            Fixture  : Buat tabel DynamoDB + insert 2 mahasiswa
│                                            Test 1   : statusCode harus 200
│                                            Test 2   : body response harus berisi data (tidak kosong)
│                                            Teardown : Hapus tabel setelah semua test selesai
│
├── 📄 s3-policy-20230001.json           ← [Soal 39c] IAM Custom Policy JSON
│                                            Allow    : s3:GetObject
│                                            Allow    : s3:ListBucket
│                                            Resource : arn:aws:s3:::mahasiswa-20230001-bucket
│                                            Deny     : semua aksi S3 lainnya (implicit)
│
├── 📄 trust-policy.json                 ← [Soal 39d] IAM Role Trust Policy untuk Lambda
│                                            Principal: lambda.amazonaws.com
│                                            Action   : sts:AssumeRole
│                                            Effect   : Allow
│
├── 📄 README.txt                        ← [Soal 39b] File yang di-upload ke S3 bucket
│                                            Isi      : Nama mahasiswa, NIM, mata kuliah, dosen
│
├── 📄 setup_infrastructure.sh           ← Script bash otomatis untuk semua langkah soal 39
│                                            Menjalankan : 39a → 39b → 39c → 39d → 39e secara urut
│
├── 📄 requirements.txt                  ← Daftar semua dependencies Python yang dibutuhkan
│                                            Berisi   : localstack, awscli-local, boto3, pytest
│
└── 📄 README_PRAKTIKUM.md               ← File dokumentasi ini (yang sedang kamu baca)
```

---

## 🧰 Teknologi & Tools yang Digunakan

| Teknologi | Versi | Kegunaan dalam Praktikum |
|---|---|---|
| **LocalStack** | 3.8.1 | Emulasi layanan AWS secara lokal tanpa akun AWS nyata |
| **awscli-local** | 0.22.0 | Wrapper `awslocal` — pengganti `aws` CLI untuk LocalStack |
| **AWS Lambda** | python3.11 | Serverless function `GetStudents` untuk endpoint GET /students |
| **Amazon DynamoDB** | — | NoSQL database, tabel `mahasiswa` dengan partition key `StudentId` |
| **Amazon S3** | — | Object storage, bucket `mahasiswa-20230001-bucket` |
| **AWS IAM** | — | User `lab-user-20230001`, Role `lambda-role-20230001`, custom policy |
| **boto3** | ≥ 1.34 | AWS SDK Python untuk berinteraksi dengan DynamoDB & Lambda di test |
| **pytest** | ≥ 8.0 | Framework testing Python untuk soal 40 |
| **GitHub Actions** | — | CI/CD pipeline otomatis yang berjalan saat push ke branch `main` |
| **Docker** | ≥ 24.x | Menjalankan container LocalStack |

---

## ⚙️ Prasyarat & Instalasi

### 1. Pastikan Docker sudah berjalan

```bash
# Cek versi Docker
docker --version
# Docker version 24.x.x atau lebih baru

# Pastikan daemon aktif
docker ps
```

### 2. Install semua dependencies Python

```bash
pip install -r requirements.txt
```

Atau install satu per satu:

```bash
pip install localstack          # LocalStack CLI & daemon
pip install awscli-local        # wrapper awslocal
pip install boto3               # AWS SDK Python
pip install pytest              # framework testing
```

### 3. Verifikasi instalasi

```bash
localstack --version    # 3.8.1
awslocal --version      # aws-cli/2.x.x Python/3.11.x
python3 --version       # Python 3.11.x
pytest --version        # pytest 8.x.x
docker --version        # Docker 24.x.x
```

---

## 🚀 Cara Menjalankan

### ▶️ Opsi A — Otomatis (Semua Soal 39 Sekaligus)

```bash
# Berikan permission eksekusi pada script
chmod +x setup_infrastructure.sh

# Jalankan semua langkah soal 39 (a s/d e) sekaligus
./setup_infrastructure.sh
```

Script ini akan otomatis menjalankan semua langkah dari **39a sampai 39e** secara berurutan termasuk verifikasi tiap step.

---

### ▶️ Opsi B — Manual Step by Step

---

#### 📌 Soal 39a — Start LocalStack & Verifikasi Semua Service (1 Poin)

**Tujuan:** Menjalankan LocalStack sebagai background daemon dan memastikan semua AWS service yang dibutuhkan aktif.

```bash
# Install LocalStack dan awslocal jika belum ada
pip install localstack awscli-local --break-system-packages

# Start LocalStack sebagai background daemon (-d = detached/background)
localstack start -d

# Tunggu beberapa detik agar semua service inisialisasi
sleep 5

# Lihat status semua service yang tersedia
localstack status services

# Verifikasi via HTTP health endpoint (harus return JSON dengan status "available")
curl -s http://localhost:4566/_localstack/health | python3 -m json.tool
```

**Output yang diharapkan dari `localstack status services`:**

```
┌─────────────────┬───────────────────┐
│ Service         │ Status            │
├─────────────────┼───────────────────┤
│ dynamodb        │ ✔ available       │
│ iam             │ ✔ available       │
│ lambda          │ ✔ available       │
│ s3              │ ✔ available       │
│ sts             │ ✔ available       │
│ cloudwatch      │ ✔ available       │
│ logs            │ ✔ available       │
│ events          │ ✔ available       │
│ sns             │ ✔ available       │
└─────────────────┴───────────────────┘
```

> **Catatan:** LocalStack berjalan di port `4566`. Semua perintah `awslocal` otomatis mengarah ke endpoint ini.

---

#### 📌 Soal 39b — Buat S3 Bucket & Upload README.txt (1 Poin)

**Tujuan:** Membuat S3 bucket dengan nama sesuai format soal dan mengupload file yang berisi identitas mahasiswa.

```bash
# Buat file README.txt dengan isi nama mahasiswa
cat > README.txt << 'EOF'
Nama Mahasiswa : Budi Santoso
NIM            : 20230001
Mata Kuliah    : IF1405 - Infrastruktur Cloud dan Sistem Terdistribusi
Dosen          : Dikky Suryadi S.Kom, M.Kom
Institusi      : Institut Sains dan Teknologi Nasional (ISTN)
Kelas          : Hybrid
EOF

# Tampilkan isi file untuk verifikasi
cat README.txt

# Buat S3 bucket bernama mahasiswa-[NIM]-bucket
awslocal s3 mb s3://mahasiswa-20230001-bucket

# Upload file README.txt ke dalam bucket
awslocal s3 cp README.txt s3://mahasiswa-20230001-bucket/README.txt

# Verifikasi — list isi bucket
awslocal s3 ls s3://mahasiswa-20230001-bucket

# Verifikasi — baca kembali isi file dari S3
awslocal s3 cp s3://mahasiswa-20230001-bucket/README.txt - 
```

**Output yang diharapkan:**

```
make_bucket: mahasiswa-20230001-bucket
upload: ./README.txt to s3://mahasiswa-20230001-bucket/README.txt
2026-05-20 09:15:32       173 README.txt
```

---

#### 📌 Soal 39c — IAM User + Custom Policy S3 Read-Only (2 Poin)

**Tujuan:** Membuat IAM User dengan policy custom yang hanya mengizinkan operasi baca pada bucket yang sudah dibuat.

```bash
# Step 1: Buat IAM User
awslocal iam create-user --user-name lab-user-20230001

# Step 2: Tampilkan isi file policy JSON
cat s3-policy-20230001.json
```

**Isi file `s3-policy-20230001.json`:**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3ReadOnly",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::mahasiswa-20230001-bucket",
                "arn:aws:s3:::mahasiswa-20230001-bucket/*"
            ]
        }
    ]
}
```

> **Penjelasan Policy:**
> - `s3:GetObject` — mengizinkan download/baca file dari dalam bucket
> - `s3:ListBucket` — mengizinkan melihat daftar file di bucket
> - Aksi lain seperti `s3:PutObject`, `s3:DeleteObject` secara **implisit ditolak** (not allowed)

```bash
# Step 3: Daftarkan custom policy ke IAM
awslocal iam create-policy \
    --policy-name S3ReadOnlyPolicy-20230001 \
    --policy-document file://s3-policy-20230001.json

# Step 4: Attach policy ke user lab-user-20230001
awslocal iam attach-user-policy \
    --user-name lab-user-20230001 \
    --policy-arn arn:aws:iam::000000000000:policy/S3ReadOnlyPolicy-20230001

# Step 5: Verifikasi — cek policy yang sudah di-attach ke user
awslocal iam list-attached-user-policies --user-name lab-user-20230001
```

**Output yang diharapkan:**

```json
{
    "AttachedPolicies": [
        {
            "PolicyName": "S3ReadOnlyPolicy-20230001",
            "PolicyArn": "arn:aws:iam::000000000000:policy/S3ReadOnlyPolicy-20230001"
        }
    ]
}
```

---

#### 📌 Soal 39d — IAM Role Lambda + DynamoDB Table (2 Poin)

**Tujuan:** Membuat IAM Role yang bisa di-assume oleh Lambda, dan membuat tabel DynamoDB untuk menyimpan data mahasiswa.

```bash
# Tampilkan isi trust policy
cat trust-policy.json
```

**Isi file `trust-policy.json`:**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

> **Penjelasan Trust Policy:**
> Trust policy mendefinisikan **siapa yang boleh menggunakan role ini**.
> Dengan `Principal: lambda.amazonaws.com`, hanya Lambda function yang boleh assume role ini.
> Ini adalah syarat wajib agar Lambda bisa mengakses resource AWS lain (seperti DynamoDB).

```bash
# Step 1: Buat IAM Role untuk Lambda
awslocal iam create-role \
    --role-name lambda-role-20230001 \
    --assume-role-policy-document file://trust-policy.json

# Step 2: Attach policy DynamoDB Full Access ke role (agar Lambda bisa baca/tulis DynamoDB)
awslocal iam attach-role-policy \
    --role-name lambda-role-20230001 \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# Step 3: Buat tabel DynamoDB 'mahasiswa'
# - Partition key (Primary Key): StudentId bertipe String (S)
# - Billing mode: PAY_PER_REQUEST (on-demand, tidak perlu set kapasitas)
awslocal dynamodb create-table \
    --table-name mahasiswa \
    --attribute-definitions AttributeName=StudentId,AttributeType=S \
    --key-schema AttributeName=StudentId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Step 4: Verifikasi tabel berhasil dibuat
awslocal dynamodb list-tables

# Step 5: Lihat detail tabel
awslocal dynamodb describe-table --table-name mahasiswa
```

**Output yang diharapkan dari `list-tables`:**

```json
{
    "TableNames": [
        "mahasiswa"
    ]
}
```

---

#### 📌 Soal 39e — Deploy Lambda Function GetStudents (2 Poin)

**Tujuan:** Membuat Lambda function Python yang membaca semua data mahasiswa dari DynamoDB, lalu deploy ke LocalStack.

**Isi file `handler.py`:**

```python
import json
import boto3
import os

def lambda_handler(event, context):
    """
    Lambda function untuk GET /students
    Mengambil semua item dari DynamoDB tabel 'mahasiswa'
    """
    try:
        endpoint = os.environ.get(
            'DYNAMODB_ENDPOINT', 
            'http://localhost:4566'
        )
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=endpoint,
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        table = dynamodb.Table('mahasiswa')

        # Scan semua item dengan pagination
        students = []
        response = table.scan()
        students.extend(response.get('Items', []))

        # Handle pagination jika data > 1MB
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            students.extend(response.get('Items', []))

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'students': students,
                'count': len(students)
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

```bash
# Step 1: Zip handler.py menjadi function.zip
zip function.zip handler.py

# Step 2: Deploy Lambda ke LocalStack
awslocal lambda create-function \
    --function-name GetStudents \
    --runtime python3.11 \
    --handler handler.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::000000000000:role/lambda-role-20230001 \
    --environment Variables="{DYNAMODB_ENDPOINT=http://localhost:4566}" \
    --timeout 30 \
    --memory-size 128

# Step 3: Insert data uji ke DynamoDB
awslocal dynamodb put-item \
    --table-name mahasiswa \
    --item '{
        "StudentId":  {"S": "20230001"},
        "Nama":       {"S": "Budi Santoso"},
        "Jurusan":    {"S": "Teknik Informatika"},
        "Semester":   {"N": "5"},
        "IPK":        {"S": "3.75"}
    }'

awslocal dynamodb put-item \
    --table-name mahasiswa \
    --item '{
        "StudentId":  {"S": "20230002"},
        "Nama":       {"S": "Siti Rahayu"},
        "Jurusan":    {"S": "Sistem Informasi"},
        "Semester":   {"N": "3"},
        "IPK":        {"S": "3.60"}
    }'

# Step 4: Invoke Lambda dan lihat hasilnya
awslocal lambda invoke \
    --function-name GetStudents \
    --payload '{"httpMethod": "GET", "path": "/students"}' \
    output.json

# Tampilkan hasil invoke
cat output.json | python3 -m json.tool
```

**Output yang diharapkan:**

```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"students\": [{\"StudentId\": \"20230001\", \"Nama\": \"Budi Santoso\", ...}, {\"StudentId\": \"20230002\", ...}], \"count\": 2}"
}
```

---

### ▶️ Soal 40 — GitHub Actions CI/CD (Dijalankan Secara Lokal)

> **Catatan Soal:** Soal ini meminta GitHub Actions workflow yang "buat ajar menjadi Localhost" — artinya cukup menunjukkan file YAML sebagai referensi dan menjalankan **pytest secara lokal** sebagai simulasinya. Tidak perlu push ke GitHub sungguhan.

---

#### 📌 Soal 40a & 40b — File YAML GitHub Actions (4 Poin)

**Isi file `.github/workflows/test.yml`:**

```yaml
name: LocalStack Lambda CI

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      localstack:
        image: localstack/localstack:3.8.1
        ports:
          - 4566:4566
        env:
          SERVICES: s3,iam,lambda,dynamodb,sts
          DEFAULT_REGION: us-east-1
          AWS_DEFAULT_REGION: us-east-1
          AWS_ACCESS_KEY_ID: test
          AWS_SECRET_ACCESS_KEY: test
        options: >-
          --health-cmd "curl -f http://localhost:4566/_localstack/health || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 10

    env:
      AWS_ACCESS_KEY_ID: test
      AWS_SECRET_ACCESS_KEY: test
      AWS_DEFAULT_REGION: us-east-1
      AWS_ENDPOINT_URL: http://localhost:4566

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install awscli-local boto3 pytest localstack

      - name: Wait for LocalStack to be ready
        run: |
          echo "Waiting for LocalStack..."
          for i in $(seq 1 30); do
            if curl -sf http://localhost:4566/_localstack/health > /dev/null; then
              echo "LocalStack is ready!"
              break
            fi
            echo "Attempt $i/30 — waiting..."
            sleep 3
          done

      - name: Setup infrastructure (S3, IAM, Lambda, DynamoDB)
        run: |
          chmod +x setup_infrastructure.sh
          ./setup_infrastructure.sh

      - name: Run pytest tests
        run: |
          pytest test_lambda.py -v --tb=short
```

---

#### 📌 Soal 40c — File test_lambda.py dengan pytest (3 Poin)

**Isi file `test_lambda.py`:**

```python
import json
import boto3
import pytest

ENDPOINT = "http://localhost:4566"
REGION   = "us-east-1"
TABLE    = "mahasiswa"

AWS_CREDS = {
    "endpoint_url":          ENDPOINT,
    "region_name":           REGION,
    "aws_access_key_id":     "test",
    "aws_secret_access_key": "test",
}

@pytest.fixture(scope="module")
def dynamodb_table():
    """
    Fixture: buat tabel DynamoDB + insert 2 data mahasiswa.
    Cleanup otomatis setelah semua test dalam module selesai.
    """
    dynamodb = boto3.resource('dynamodb', **AWS_CREDS)

    # Buat tabel mahasiswa
    table = dynamodb.create_table(
        TableName=TABLE,
        AttributeDefinitions=[
            {'AttributeName': 'StudentId', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'StudentId', 'KeyType': 'HASH'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()

    # Insert 2 data mahasiswa uji
    table.put_item(Item={
        'StudentId': '20230001',
        'Nama':      'Budi Santoso',
        'Jurusan':   'Teknik Informatika',
        'Semester':  5
    })
    table.put_item(Item={
        'StudentId': '20230002',
        'Nama':      'Siti Rahayu',
        'Jurusan':   'Sistem Informasi',
        'Semester':  3
    })

    yield table

    # Teardown: hapus tabel setelah semua test selesai
    table.delete()


def test_get_students_returns_200(dynamodb_table):
    """Test: Lambda harus mengembalikan HTTP statusCode 200."""
    client = boto3.client('lambda', **AWS_CREDS)

    response = client.invoke(
        FunctionName='GetStudents',
        Payload=json.dumps({'httpMethod': 'GET', 'path': '/students'})
    )

    result = json.loads(response['Payload'].read())
    assert result['statusCode'] == 200, \
        f"Expected 200, got {result['statusCode']}"


def test_get_students_data_not_empty(dynamodb_table):
    """Test: Response body harus berisi minimal 1 data mahasiswa."""
    client = boto3.client('lambda', **AWS_CREDS)

    response = client.invoke(
        FunctionName='GetStudents',
        Payload=json.dumps({'httpMethod': 'GET', 'path': '/students'})
    )

    result  = json.loads(response['Payload'].read())
    body    = json.loads(result['body'])
    students = body.get('students', [])

    assert len(students) > 0, \
        "Expected at least 1 student, got empty list"
    assert body['count'] == len(students), \
        "Count field tidak sesuai dengan jumlah data"
```

**Cara menjalankan pytest lokal:**

```bash
# Install pytest dan boto3
pip install pytest boto3 --break-system-packages

# Jalankan dengan output verbose
pytest test_lambda.py -v --tb=short
```

**Output yang diharapkan:**

```
====================== test session starts ======================
platform linux -- Python 3.11.x, pytest-8.x.x
rootdir: /home/aflin/aflin
collected 2 items

test_lambda.py::test_get_students_returns_200      PASSED  [ 50%]
test_lambda.py::test_get_students_data_not_empty   PASSED  [100%]

====================== 2 passed in 1.84s ======================
```

---

## 📋 Penjelasan Detail Setiap File

### `handler.py` — Lambda Function
File ini adalah **inti dari Lambda function** yang di-deploy ke LocalStack.

- **Entry point:** `lambda_handler(event, context)` — dipanggil otomatis oleh Lambda runtime
- **Endpoint:** Melayani `GET /students` — mengembalikan semua data mahasiswa dari DynamoDB
- **Pagination:** Menangani `LastEvaluatedKey` secara otomatis agar semua data terbaca meski jumlahnya besar (> 1MB per scan)
- **Error handling:** Mengembalikan `statusCode 500` dengan pesan error jika terjadi exception
- **Konfigurasi:** Membaca `DYNAMODB_ENDPOINT` dari environment variable untuk koneksi ke LocalStack

### `test_lambda.py` — pytest Test Suite
File ini berisi **automated test** untuk memverifikasi bahwa Lambda berjalan dengan benar.

- **Fixture `dynamodb_table`** dengan `scope="module"`: Setup tabel + insert 2 data mahasiswa sebelum test dimulai, cleanup (delete table) setelah semua test selesai
- **`test_get_students_returns_200`**: Memastikan hasil invoke Lambda memiliki `statusCode` = 200 (HTTP OK)
- **`test_get_students_data_not_empty`**: Memastikan body response berisi array `students` yang tidak kosong dan `count` sesuai

### `.github/workflows/test.yml` — CI/CD Pipeline
File ini mendefinisikan **GitHub Actions workflow** yang berjalan otomatis saat ada push ke `main`.

- **Trigger:** `on: push: branches: [main]`
- **Service:** LocalStack dijalankan sebagai Docker container dengan health check
- **Environment:** AWS credentials dummy (`test/test`) diarahkan ke LocalStack endpoint (`http://localhost:4566`)
- **Steps:** Checkout → Python setup → Install deps → Health check loop → Setup infra → pytest

### `s3-policy-20230001.json` — IAM Policy
Policy ini memberikan **akses terbatas hanya baca** ke S3 bucket:

- ✅ `s3:GetObject` — bisa download/membaca file dari bucket
- ✅ `s3:ListBucket` — bisa melihat daftar file dalam bucket
- ❌ `s3:PutObject` — tidak bisa upload file (implicit deny)
- ❌ `s3:DeleteObject` — tidak bisa menghapus file (implicit deny)

### `trust-policy.json` — IAM Trust Policy
Mendefinisikan **entitas mana yang boleh menggunakan role** `lambda-role-20230001`. Hanya `lambda.amazonaws.com` yang diizinkan (`sts:AssumeRole`), sehingga hanya Lambda function yang dapat menggunakan role ini untuk mengakses DynamoDB.

### `setup_infrastructure.sh` — Script Otomatis
Script bash yang menjalankan semua langkah soal 39 (a–e) secara berurutan otomatis. Berguna untuk reset dan setup ulang environment dengan cepat tanpa mengetik perintah satu per satu.

---

## 📊 Ringkasan Poin Soal

| No | Sub-soal | Deskripsi | File Terkait | Poin |
|:--:|----------|-----------|-------------|:----:|
| 39a | Start LocalStack | Start daemon + verifikasi semua service aktif | — | 1 |
| 39b | S3 Bucket | Buat `mahasiswa-20230001-bucket` + upload `README.txt` | `README.txt` | 1 |
| 39c | IAM User & Policy | `lab-user-20230001` + policy S3 read-only + attach | `s3-policy-20230001.json` | 2 |
| 39d | IAM Role & DynamoDB | `lambda-role-20230001` trust Lambda + tabel `mahasiswa` | `trust-policy.json` | 2 |
| 39e | Lambda Deploy | `handler.py` → zip → deploy `GetStudents` → invoke test | `handler.py` | 2 |
| 40a | GitHub Actions YAML | Trigger push→main, LocalStack Docker service, env AWS | `test.yml` | 2 |
| 40b | CI/CD Steps | Install deps, health-check loop, setup infra, run pytest | `test.yml` | 2 |
| 40c | pytest Test File | Fixture DynamoDB+insert 2 mhs, 2 test cases, cleanup | `test_lambda.py` | 3 |
| | | | **Total** | **15** |

---

## 🔧 Troubleshooting

### ❗ LocalStack tidak mau start

```bash
# Pastikan Docker daemon berjalan
docker ps

# Cek apakah port 4566 sudah dipakai proses lain
lsof -i :4566

# Stop LocalStack lama, lalu restart
localstack stop
localstack start -d
```

### ❗ `awslocal: command not found`

```bash
pip install awscli-local
# Jika pakai sistem Python (bukan venv):
pip install awscli-local --break-system-packages
```

### ❗ Lambda gagal invoke — `ResourceNotFoundException`

```bash
# Cek apakah tabel DynamoDB sudah ada
awslocal dynamodb list-tables

# Jika belum ada, buat ulang:
awslocal dynamodb create-table \
    --table-name mahasiswa \
    --attribute-definitions AttributeName=StudentId,AttributeType=S \
    --key-schema AttributeName=StudentId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

### ❗ pytest gagal — `EndpointConnectionError`

```bash
# Pastikan LocalStack masih berjalan
localstack status

# Cek health endpoint
curl -s http://localhost:4566/_localstack/health | python3 -m json.tool
```

### ❗ Lambda function tidak ditemukan saat pytest

```bash
# Verifikasi Lambda sudah ter-deploy
awslocal lambda list-functions

# Jika belum ada, jalankan ulang:
zip function.zip handler.py
awslocal lambda create-function \
    --function-name GetStudents \
    --runtime python3.11 \
    --handler handler.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::000000000000:role/lambda-role-20230001
```

---

## 📚 Referensi

- [LocalStack Documentation](https://docs.localstack.cloud)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [AWS DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

<div align="center">

**Institut Sains dan Teknologi Nasional (ISTN)**

Jl. Moh. Kahfi II, Bhumi Srengseng Indah, Jagakarsa, Jakarta Selatan 12640

*UTS Genap 2025/2026*

</div>
