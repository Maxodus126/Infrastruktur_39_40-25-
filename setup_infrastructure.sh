#!/bin/bash
# ============================================================
# IF1405 - Infrastruktur Cloud dan Sistem Terdistribusi
# Script setup lengkap LocalStack (Soal 39)
# Nama  : Budi Santoso
# NIM   : 20230001
# ============================================================

set -e  # Stop jika ada error

ENDPOINT="http://localhost:4566"
NIM="20230001"
BUCKET="mahasiswa-${NIM}-bucket"

echo "=================================================="
echo " IF1405 - LocalStack Setup - NIM: $NIM"
echo "=================================================="

# ── 39a: Start LocalStack ──
echo ""
echo "[39a] Starting LocalStack..."
localstack start -d
echo "Menunggu LocalStack siap..."
sleep 5
localstack status services

# ── 39b: S3 Bucket ──
echo ""
echo "[39b] Membuat S3 bucket: $BUCKET"
awslocal s3 mb s3://$BUCKET
awslocal s3 cp README.txt s3://$BUCKET/README.txt
echo "Isi bucket:"
awslocal s3 ls s3://$BUCKET

# ── 39c: IAM User + Policy ──
echo ""
echo "[39c] Membuat IAM User: lab-user-$NIM"
awslocal iam create-user --user-name lab-user-$NIM
awslocal iam create-policy \
    --policy-name S3ReadOnlyPolicy-$NIM \
    --policy-document file://s3-policy-${NIM}.json
awslocal iam attach-user-policy \
    --user-name lab-user-$NIM \
    --policy-arn arn:aws:iam::000000000000:policy/S3ReadOnlyPolicy-$NIM
echo "Policy attached ke user lab-user-$NIM"

# ── 39d: IAM Role + DynamoDB ──
echo ""
echo "[39d] Membuat IAM Role: lambda-role-$NIM"
awslocal iam create-role \
    --role-name lambda-role-$NIM \
    --assume-role-policy-document file://trust-policy.json
awslocal iam attach-role-policy \
    --role-name lambda-role-$NIM \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

echo "Membuat DynamoDB tabel: mahasiswa"
awslocal dynamodb create-table \
    --table-name mahasiswa \
    --attribute-definitions AttributeName=StudentId,AttributeType=S \
    --key-schema AttributeName=StudentId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
echo "Tabel DynamoDB:"
awslocal dynamodb list-tables

# ── 39e: Lambda ──
echo ""
echo "[39e] Deploy Lambda: GetStudents"
zip function.zip handler.py
awslocal lambda create-function \
    --function-name GetStudents \
    --runtime python3.11 \
    --handler handler.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::000000000000:role/lambda-role-$NIM \
    --environment Variables="{DYNAMODB_ENDPOINT=$ENDPOINT}" \
    --timeout 30 \
    --memory-size 128

echo "Insert data uji..."
awslocal dynamodb put-item \
    --table-name mahasiswa \
    --item '{"StudentId":{"S":"20230001"},"Nama":{"S":"Budi Santoso"},"Jurusan":{"S":"Teknik Informatika"},"Semester":{"N":"5"}}'
awslocal dynamodb put-item \
    --table-name mahasiswa \
    --item '{"StudentId":{"S":"20230002"},"Nama":{"S":"Siti Rahayu"},"Jurusan":{"S":"Teknik Informatika"},"Semester":{"N":"5"}}'

echo "Invoke Lambda GetStudents..."
awslocal lambda invoke \
    --function-name GetStudents \
    --payload '{"httpMethod":"GET","path":"/students"}' \
    output.json
cat output.json

echo ""
echo "=================================================="
echo " ✅ SEMUA INFRASTRUKTUR BERHASIL DIBUAT"
echo "=================================================="
