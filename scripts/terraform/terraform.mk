# This file is for you! Edit it to implement your own Terraform make targets.

# ==============================================================================
# Custom implementation - implementation of a make target should not exceed 5 lines of effective code.
# In most cases there should be no need to modify the existing make targets.

TF_ENV ?= dev
STACK ?= ${stack}
TERRAFORM_STACK ?= $(or ${STACK}, infrastructure/environments/${TF_ENV})
dir ?= ${TERRAFORM_STACK}

dev:
	$(eval CONFIG=dev)

terraform-init: # Initialise Terraform - make <env> terraform-init
	terraform -chdir=infrastructure/terraform init

terraform-plan: terraform-init # Plan Terraform changes - make <env> terraform-plan
	terraform -chdir=infrastructure/terraform plan -var-file ../environments/${CONFIG}/variables.tfvars

terraform-apply: # Apply Terraform changes - make <env> terraform-apply
	terraform -chdir=infrastructure/terraform plan -var-file ../environments/${CONFIG}/variables.tfvars

terraform-destroy: # Destroy Terraform resources - make <env> terraform-destroy
	terraform -chdir=infrastructure/terraform destroy -var-file ../environments/${CONFIG}/variables.tfvars

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
