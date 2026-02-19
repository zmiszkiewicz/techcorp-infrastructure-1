# TechCorp Infrastructure

Production-ready infrastructure automation using **Terraform**, **Ansible**, and **Infoblox Universal DDI**.

This repository demonstrates enterprise CI/CD pipelines that provision AWS infrastructure AND integrate with Infoblox Universal DDI for IP management and DNS — the way real DevOps teams do it.

## Scenario: TechCorp Digital Transformation

TechCorp is a manufacturing company undergoing digital transformation:

1. **Greenfield:** Deploying a new cloud-native inventory management application on AWS
2. **Hybrid Cloud:** Migrating legacy on-prem DNS/IPAM to Universal DDI

Your job: Build a production-ready CI/CD pipeline that provisions AWS infrastructure AND integrates with Infoblox Universal DDI for IP management and DNS.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                       │
│              (GitHub Actions / CI/CD Pipeline)               │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌─────────────────────┐          ┌─────────────────────┐
│     TERRAFORM       │          │      ANSIBLE        │
│   (Day-0 / Day-1)   │          │      (Day-2)        │
│                     │          │                     │
│ • IP Spaces         │          │ • Bulk DNS records  │
│ • Address Blocks    │          │ • IPAM allocations  │
│ • DNS Views/Zones   │          │ • Legacy migration  │
│ • AWS VPC/Subnets   │          │ • Remediation       │
└─────────────────────┘          └─────────────────────┘
         │                                    │
         └────────────────┬───────────────────┘
                          ▼
              ┌─────────────────────┐
              │  INFOBLOX UNIVERSAL │
              │        DDI          │
              │   (API-First)       │
              └─────────────────────┘
```

## Lab Environment (Instruqt)

This repo is used as the student code repository for the **Auto 1 — Production-Ready Infrastructure Automation** Instruqt lab.

**When running in the lab, everything is pre-configured for you:**
- Terraform, Ansible, AWS CLI, and GitHub CLI are pre-installed
- The repo is pre-cloned to `/root/lab/techcorp-infrastructure`
- AWS credentials and Infoblox API keys are injected via environment variables
- An S3 remote backend is provisioned per student for Terraform state
- A dedicated Infoblox sandbox tenant is created per student

You do **not** need to install anything or configure credentials manually — just follow the challenge instructions.

### Lab Challenges

| # | Challenge | What You Do | Time |
|---|-----------|-------------|------|
| 1 | **The Journey Begins** | Experience manual ClickOps pain | 5 min |
| 2 | **Git-Based Foundation** | Explore the repo structure and architecture | 10 min |
| 3 | **Terraform — IPAM & DNS** | Provision AWS + register in Infoblox IPAM + DNS | 20 min |
| 4 | **Ansible — Day-2 Operations** | Bulk DNS records, next-available IP allocation | 15 min |
| 5 | **Ansible — Migration** | Migrate legacy records, clean up orphans | 15 min |
| 6 | **Drift & CI/CD Orchestration** | Drift detection, full-stack pipeline, PR workflow | 20 min |

### The Journey

```
UI (pain) → Scripts (fragile) → Terraform (intent) → Ansible (day-2) → CI/CD (orchestration)
  Ch.1          Ch.1                Ch.2-3              Ch.4-5              Ch.6
```

## Repository Structure

```
techcorp-infrastructure/
├── .github/workflows/
│   ├── terraform-plan.yml          # PR triggers plan + posts to PR comment
│   ├── terraform-apply.yml         # Merge to main triggers apply
│   └── full-stack-deploy.yml       # Full orchestration (TF + Ansible + Validate)
├── terraform/
│   ├── environments/
│   │   ├── dev/                    # Dev: 172.20.0.0/16
│   │   └── prod/                   # Prod: 10.200.0.0/16
│   └── modules/
│       ├── aws-networking/         # VPC, Subnets, IGW, Route Tables
│       ├── infoblox-ipam/          # IP Spaces, Address Blocks, Subnets
│       └── infoblox-dns/           # Views, Zones, Records
├── ansible/
│   ├── ansible.cfg
│   ├── inventory/hosts.yml
│   ├── group_vars/all.yml
│   └── playbooks/
│       ├── dns-records.yml         # Bulk DNS record creation
│       ├── ipam-allocate.yml       # Next-available IP/subnet allocation
│       ├── migrate-legacy.yml      # Legacy on-prem migration
│       ├── cleanup-orphans.yml     # Remove unmanaged orphan records
│       └── validate-deployment.yml # End-to-end validation
├── demo/
│   ├── manual_dns.py               # "Bad" script — shows why automation matters
│   ├── good_example.tf             # "Good" Terraform — contrast with the script
│   └── ip_spreadsheet.csv          # Fake IP spreadsheet — shows IPAM chaos
├── scripts/
│   ├── trigger-cicd.sh             # Forks repo + sets secrets + triggers pipeline
│   ├── sandbox_api.py              # Infoblox sandbox API client
│   ├── create_sandbox.py           # Creates per-student sandbox tenant
│   ├── create_user.py              # Creates user in sandbox
│   ├── deploy_api_key.py           # Generates API key + exports to env
│   ├── delete_user.py              # Cleanup: removes user
│   └── delete_sandbox.py           # Cleanup: removes sandbox
└── docs/
    ├── INSTALL-MAC.md              # Local setup (macOS)
    ├── INSTALL-WINDOWS.md          # Local setup (Windows/WSL)
    └── TROUBLESHOOTING.md
```

## When to Use What

| Tool | Role | Use For |
|------|------|---------|
| **Terraform** | Day-0/Day-1 Builder | Infrastructure provisioning, state-tracked resources |
| **Ansible** | Day-2 Operations | Bulk changes, migrations, remediation (stateless) |
| **CI/CD Pipeline** | Orchestrator | Coordinating Terraform + Ansible + validation |

## CI/CD Pipeline

The `full-stack-deploy.yml` workflow orchestrates the entire deployment:

```
┌─────────────────┐   ┌──────────────────────────────────┐   ┌─────────────────┐   ┌──────────────┐
│   TERRAFORM     │   │  ANSIBLE DNS   (parallel)        │   │   VALIDATE      │   │   SUMMARY    │
│   AWS + IPAM    │──▶│  ANSIBLE IPAM  (parallel)        │──▶│   End-to-End    │──▶│   Report     │
│   + DNS         │   │                                  │   │                 │   │              │
└─────────────────┘   └──────────────────────────────────┘   └─────────────────┘   └──────────────┘
```

1. **Terraform** provisions AWS infrastructure + registers in Infoblox IPAM + creates DNS zones
2. **Ansible DNS** creates application DNS records (runs in parallel with IPAM)
3. **Ansible IPAM** allocates IPs for new instances (runs in parallel with DNS)
4. **Validation** verifies the entire stack end-to-end
5. **Summary** posts deployment results

### PR Workflow

| Trigger | Workflow | What Happens |
|---------|----------|-------------|
| PR to `main` (terraform/** paths) | `terraform-plan.yml` | Format check + validate + plan posted as PR comment |
| Push to `main` (terraform/** paths) | `terraform-apply.yml` | Plan + apply the change |
| Manual dispatch | `full-stack-deploy.yml` | Full stack: TF + Ansible + Validate + Summary |

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `BLOXONE_API_KEY` | Infoblox Universal DDI API key |
| `BLOXONE_CSP_URL` | Infoblox CSP portal URL |
| `S3_BUCKET_NAME` | S3 bucket for Terraform remote state |

> In the Instruqt lab, the `scripts/trigger-cicd.sh` script configures all 5 secrets automatically on your fork.

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues and solutions.

<details>
<summary><strong>Running Locally (Outside the Lab)</strong></summary>

If you want to run this repo on your own machine (for self-study, demos, or development), you'll need to install the prerequisites and configure credentials manually.

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5.0
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/) >= 2.14
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with credentials
- Infoblox Universal DDI API key
- An S3 bucket for Terraform remote state

> See [docs/INSTALL-MAC.md](docs/INSTALL-MAC.md) or [docs/INSTALL-WINDOWS.md](docs/INSTALL-WINDOWS.md) for step-by-step installation guides.

### Setup

```bash
# Clone the repo
git clone https://github.com/iracic82/techcorp-infrastructure.git
cd techcorp-infrastructure

# Set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
export BLOXONE_API_KEY="your-api-key"
export BLOXONE_CSP_URL="https://csp.infoblox.com"

# Install the Infoblox Ansible collection
pip3 install universal-ddi-python-client
ansible-galaxy collection install infoblox.universal_ddi

# Update backend.tf with your S3 bucket name, then:
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

### Running Ansible Playbooks Locally

```bash
# Get outputs from Terraform
cd terraform/environments/dev
export ZONE_ID=$(terraform output -raw zone_id)
export IP_SPACE_ID=$(terraform output -raw ip_space_id)
export ADDRESS_BLOCK_ID=$(terraform output -raw address_block_id)
export APP_SUBNET_ID=$(terraform output -json ipam_subnet_ids | jq -r '.app')

# Run playbooks
cd ../../..
ansible-playbook ansible/playbooks/dns-records.yml -e "zone_id=$ZONE_ID"
ansible-playbook ansible/playbooks/ipam-allocate.yml \
  -e "ip_space_id=$IP_SPACE_ID" \
  -e "address_block_id=$ADDRESS_BLOCK_ID" \
  -e "app_subnet_id=$APP_SUBNET_ID"
```

</details>

## License

Internal use only — Infoblox Sales Engineering.
