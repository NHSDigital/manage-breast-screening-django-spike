# This file is for you! Edit it to implement your own Terraform make targets.

# ==============================================================================
# Custom implementation - implementation of a make target should not exceed 5 lines of effective code.
# In most cases there should be no need to modify the existing make targets.

DOCKER_IMAGE=ghcr.io/nhsdigital/manage-breast-screening-django-spike

dev:
	$(eval include infrastructure/environments/dev/variables.sh)

ci:
	$(eval AUTO_APPROVE=-auto-approve)
	$(eval SKIP_AZURE_LOGIN=true)

set-azure-account:
	[ "${SKIP_AZURE_LOGIN}" != "true" ] && az account set -s ${AZURE_SUBSCRIPTION} || true

terraform-init: # Initialise Terraform - make <env> terraform-init
	$(if ${ARM_SUBSCRIPTION_ID},,$(eval export ARM_SUBSCRIPTION_ID=$(shell az account show --query id --output tsv)))

	terraform -chdir=infrastructure/terraform init -upgrade -reconfigure \
		-backend-config=resource_group_name=${RESOURCE_GROUP_NAME} \
		-backend-config=storage_account_name=${STORAGE_ACCOUNT_NAME} \
		-backend-config=key=${ENVIRONMENT}.tfstate

	$(eval export TF_VAR_docker_image=${DOCKER_IMAGE}:${DOCKER_IMAGE_TAG})

terraform-plan: terraform-init # Plan Terraform changes - make <env> terraform-plan DOCKER_IMAGE_TAG=abcd123
	terraform -chdir=infrastructure/terraform plan -var-file ../environments/${CONFIG}/variables.tfvars

terraform-apply: terraform-init # Apply Terraform changes - make <env> terraform-apply DOCKER_IMAGE_TAG=abcd123
	terraform -chdir=infrastructure/terraform apply -var-file ../environments/${CONFIG}/variables.tfvars ${AUTO_APPROVE}

terraform-destroy: # Destroy Terraform resources - make <env> terraform-destroy
	terraform -chdir=infrastructure/terraform destroy -var-file ../environments/${CONFIG}/variables.tfvars ${AUTO_APPROVE}

terraform-fmt: # Format Terraform files - optional: terraform_dir|dir=[path to a directory where the command will be executed, relative to the project's top-level directory, default is one of the module variables or the example directory, if not set], terraform_opts|opts=[options to pass to the Terraform fmt command, default is '-recursive'] @Quality
	make _terraform cmd="fmt" \
		dir=$(or ${terraform_dir}, ${dir}) \
		opts=$(or ${terraform_opts}, ${opts})

terraform-validate: # Validate Terraform configuration - optional: terraform_dir|dir=[path to a directory where the command will be executed, relative to the project's top-level directory, default is one of the module variables or the example directory, if not set], terraform_opts|opts=[options to pass to the Terraform validate command, default is none/empty] @Quality
	make _terraform cmd="validate" \
		dir=$(or ${terraform_dir}, ${dir}) \
		opts=$(or ${terraform_opts}, ${opts})

clean:: # Remove Terraform files (terraform) - optional: terraform_dir|dir=[path to a directory where the command will be executed, relative to the project's top-level directory, default is one of the module variables or the example directory, if not set] @Operations
	make _terraform cmd="clean" \
		dir=$(or ${terraform_dir}, ${dir}) \
		opts=$(or ${terraform_opts}, ${opts})

_terraform: # Terraform command wrapper - mandatory: cmd=[command to execute]; optional: dir=[path to a directory where the command will be executed, relative to the project's top-level directory, default is one of the module variables or the example directory, if not set], opts=[options to pass to the Terraform command, default is none/empty]
	dir=$(or ${dir}, ${TERRAFORM_STACK})
	source scripts/terraform/terraform.lib.sh
	terraform-${cmd} # 'dir' and 'opts' are accessible by the function as environment variables, if set

# ==============================================================================
# Quality checks - please DO NOT edit this section!

terraform-shellscript-lint: # Lint all Terraform module shell scripts @Quality
	for file in $$(find scripts/terraform -type f -name "*.sh"); do
		file=$${file} scripts/shellscript-linter.sh
	done

# ==============================================================================
# Configuration - please DO NOT edit this section!

terraform-install: # Install Terraform @Installation
	make _install-dependency name="terraform"

# ==============================================================================

# ${VERBOSE}.SILENT: \
# 	_terraform \
# 	clean \
# 	terraform-apply \
# 	terraform-destroy \
# 	terraform-fmt \
# 	terraform-init \
# 	terraform-install \
# 	terraform-plan \
# 	terraform-shellscript-lint \
# 	terraform-validate \
