
terraform {
    backend "s3" {
        bucket         = "yuri-devops"
        key            = "terraform.tfstate"
        region         = "us-west-2"
        dynamodb_table = "terraform-state-locking"
        encrypt        = true
    }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_db_instance" "psql" {
  identifier              = "int-db"
  engine                  = "postgres"
  instance_class          = "db.t4g.micro"
  allocated_storage       = 20
  username                = "intuser"
  password                = "Passw0rd"
  publicly_accessible     = true
  skip_final_snapshot     = true
  vpc_security_group_ids  = ["sg-02b3d29bdcd49a0cc"]
}

# Output the RDS endpoint
output "rds_endpoint" {
  value = aws_db_instance.psql.endpoint
}
