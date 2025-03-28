# This script parses all the make target descriptions and renders the help output.
HELP_SCRIPT = \
	\
	use Text::Wrap; \
	%help_info; \
	my $$max_command_length = 0; \
	my $$terminal_width = `tput cols` || 120; chomp($$terminal_width); \
	\
	while(<>){ \
		next if /^_/; \
		\
		if (/^([\w-_]+)\s*:.*\#(.*?)(@(\w+))?\s*$$/) { \
			my $$command = $$1; \
			my $$description = $$2; \
			$$description =~ s/@\w+//; \
			my $$category_key = $$4 // 'Others'; \
			(my $$category_name = $$category_key) =~ s/(?<=[a-z])([A-Z])/\ $$1/g; \
			$$category_name = lc($$category_name); \
			$$category_name =~ s/^(.)/\U$$1/; \
			\
			push @{$$help_info{$$category_name}}, [$$command, $$description]; \
			$$max_command_length = (length($$command) > 37) ? 40 : $$max_command_length; \
		} \
	} \
	\
	my $$description_width = $$terminal_width - $$max_command_length - 4; \
	$$Text::Wrap::columns = $$description_width; \
	\
	for my $$category (sort { $$a eq 'Others' ? 1 : $$b eq 'Others' ? -1 : $$a cmp $$b } keys %help_info) { \
		print "\033[1m$$category\033[0m:\n\n"; \
		for my $$item (sort { $$a->[0] cmp $$b->[0] } @{$$help_info{$$category}}) { \
			my $$description = $$item->[1]; \
			my @desc_lines = split("\n", wrap("", "", $$description)); \
			my $$first_line_description = shift @desc_lines; \
			\
			$$first_line_description =~ s/(\w+)(\|\w+)?=/\033[3m\033[93m$$1$$2\033[0m=/g; \
			\
			my $$formatted_command = $$item->[0]; \
			$$formatted_command = substr($$formatted_command, 0, 37) . "..." if length($$formatted_command) > 37; \
			\
			print sprintf("  \033[0m\033[34m%-$${max_command_length}s\033[0m%s %s\n", $$formatted_command, $$first_line_description); \
			for my $$line (@desc_lines) { \
				$$line =~ s/(\w+)(\|\w+)?=/\033[3m\033[93m$$1$$2\033[0m=/g; \
				print sprintf(" %-$${max_command_length}s  %s\n", " ", $$line); \
			} \
			print "\n"; \
		} \
	}