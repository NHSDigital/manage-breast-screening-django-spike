#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path
from django.apps import apps
from django.db.models import fields
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField
import subprocess
from django.core.management import call_command

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage_breast_screening.config.settings')
django.setup()

def get_field_type(field):
    """Convert Django field type to PlantUML type."""
    type_mapping = {
        fields.AutoField: 'Integer',
        fields.BigAutoField: 'UUID',  # Changed to match your format
        fields.BigIntegerField: 'Long',
        fields.BooleanField: 'Boolean',
        fields.CharField: 'String',
        fields.DateField: 'Date',
        fields.DateTimeField: 'DateTime',
        fields.DecimalField: 'Decimal',
        fields.EmailField: 'String',
        fields.FloatField: 'Float',
        fields.IntegerField: 'Integer',
        fields.PositiveIntegerField: 'Integer',
        fields.PositiveSmallIntegerField: 'Integer',
        fields.SmallIntegerField: 'Integer',
        fields.TextField: 'String',
        fields.TimeField: 'Time',
        fields.URLField: 'String',
        fields.UUIDField: 'UUID',
        JSONField: 'JSON',
        ForeignKey: 'UUID',
        OneToOneField: 'UUID',
        ManyToManyField: 'UUID[]'
    }
    
    # Check if field has choices
    if hasattr(field, 'choices') and field.choices:
        # Create enum name from field name
        enum_name = field.name.title().replace('_', '') + 'Type'
        return enum_name
    
    return type_mapping.get(field.__class__, 'String')

def get_relationship_type(field):
    """Get the relationship type and cardinality."""
    if isinstance(field, OneToOneField):
        return '"1"--"1"'
    elif isinstance(field, ForeignKey):
        return '"*"--"1"'
    elif isinstance(field, ManyToManyField):
        return '"*"--"*"'
    return None

def generate_graphviz_diagram():
    """Generate PNG diagram using graphviz."""
    output_png = 'docs/diagrams/database-schema.png'
    dot_path = 'docs/diagrams/database-schema.dot'
    os.makedirs('docs/diagrams', exist_ok=True)

    try:
        # First generate the DOT file
        call_command(
            'graph_models',
            'clinics',
            'participants',
            '--dot',
            '--output',
            dot_path,
            '--exclude-models=LogEntry',
            '--group-models'
        )

        # Generate PNG using graphviz
        import pygraphviz as pgv
        graph = pgv.AGraph(dot_path)
        graph.layout(prog='dot')
        graph.draw(output_png, format='png', prog='dot')

        # Clean up the intermediate DOT file
        if os.path.exists(dot_path):
            os.remove(dot_path)

        print(f'Generated PNG diagram: {output_png}')

    except Exception as e:
        print(f'Error generating PNG diagram: {str(e)}')
        raise

def generate_plantuml_diagram():
    """Generate PlantUML diagram."""
    output_puml = 'docs/diagrams/database-schema.puml'
    os.makedirs('docs/diagrams', exist_ok=True)

    try:
        # Start PlantUML content
        puml_lines = [
            '@startuml BreastScreeningSystem',
            '',
            'skinparam class {',
            '    BackgroundColor White',
            '    ArrowColor Black',
            '    BorderColor Black',
            '}',
            '',
            'skinparam stereotypeCBackgroundColor White',
            'skinparam stereotypeCBorderColor Black',
            '',
            'hide empty members',
            ''
        ]

        # Track enums to add after class definitions
        enums = {}

        # Track relationships to add after class definitions
        relationships = []

        # Get all models from installed apps
        models = apps.get_models()

        # Generate class definitions
        for model in models:
            app_label = model._meta.app_label
            model_name = model._meta.object_name

            # Skip Django's built-in models
            if app_label in ['admin', 'contenttypes', 'sessions', 'auth']:
                continue

            # Add class definition
            puml_lines.extend([
                f'class {model_name} {{',
            ])

            # Add fields
            for field in model._meta.fields:
                field_type = get_field_type(field)
                # Skip certain Django-specific fields
                if field.name in ['created', 'modified']:
                    continue
                
                if isinstance(field, (ForeignKey, OneToOneField)):
                    # Get the related model name without path
                    related_model = field.remote_field.model._meta.object_name
                    puml_lines.append(f'    - {field.name}_id: UUID <<FK>>')
                    # Add relationship with label
                    rel_type = get_relationship_type(field)
                    if rel_type:
                        relationships.append(
                            f'{model_name} {rel_type} {related_model}'
                        )
                elif field.primary_key:
                    puml_lines.append(f'    - {field.name}: UUID <<PK>>')
                else:
                    puml_lines.append(f'    - {field.name}: {field_type}')
                    # If field has choices, add them to enums
                    if hasattr(field, 'choices') and field.choices:
                        enum_name = field.name.title().replace('_', '') + 'Type'
                        enum_values = [choice[0] for choice in field.choices]
                        enums[enum_name] = enum_values

            # Handle many-to-many fields
            for field in model._meta.many_to_many:
                field_type = get_field_type(field)
                related_model = field.remote_field.model._meta.object_name
                puml_lines.append(f'    - {field.name}: UUID[]')
                rel_type = get_relationship_type(field)
                if rel_type:
                    relationships.append(
                        f'{model_name} {rel_type} {related_model}'
                    )

            puml_lines.extend([
                '}',
                ''
            ])

        # Add enums
        for enum_name, enum_values in enums.items():
            puml_lines.extend([
                f'enum {enum_name} {{',
                *[f'    {value}' for value in enum_values],
                '}',
                ''
            ])

        # Add relationships
        puml_lines.extend([''] + relationships + [''])

        # End PlantUML content
        puml_lines.append('@enduml')

        # Write PlantUML content to file
        with open(output_puml, 'w') as f:
            f.write('\n'.join(puml_lines))

        print(f'Schema diagram generated successfully:\n- PlantUML: {output_puml}')

    except Exception as e:
        print(f'Error generating schema diagram: {e}')
        raise

def generate_schema_diagrams():
    """Generate both PNG and PlantUML diagrams."""
    try:
        # Generate PNG using graphviz
        generate_graphviz_diagram()

        # Generate PlantUML diagram
        generate_plantuml_diagram()

        print('Schema diagrams generated successfully')

    except Exception as e:
        print(f'Error generating schema diagrams: {str(e)}')
        raise

if __name__ == '__main__':
    generate_schema_diagrams()
