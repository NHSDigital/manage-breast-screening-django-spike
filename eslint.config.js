import { defineConfig, globalIgnores } from 'eslint/config'
import jestDomPlugin from 'eslint-plugin-jest-dom'
import jestPlugin from 'eslint-plugin-jest'
import jsdocPlugin from 'eslint-plugin-jsdoc'
import markdownPlugin from 'eslint-plugin-markdown'
import neostandard from 'neostandard'
import tseslint from 'typescript-eslint'

export default defineConfig(
  // Global ignores
  globalIgnores([
    '**/compiled/**',
    '**/coverage/**',
    '**/staticfiles/**',
    'node_modules/**',
    'CHANGELOG.md'
  ]),

  // Base configuration with neostandard and TypeScript
  {
    extends: [
      neostandard(),
      tseslint.configs.strict,
      tseslint.configs.stylistic,
      jsdocPlugin.configs['flat/recommended']
    ]
  },

  // Main configuration for JavaScript/TypeScript files
  {
    files: ['**/*.{cjs,js,mjs}'],
    plugins: {
      jsdoc: jsdocPlugin
    },
    rules: {
      // JSDoc plugin rules
      'jsdoc/check-line-alignment': [
        'warn',
        'never',
        {
          wrapIndent: '  '
        }
      ],
      'jsdoc/check-tag-names': [
        'warn',
        {
          definedTags: ['preserve']
        }
      ],
      'jsdoc/require-jsdoc': 'off',
      'jsdoc/require-hyphen-before-param-description': 'warn',
      'jsdoc/require-param-description': 'off',
      'jsdoc/require-param-type': 'error',
      'jsdoc/require-param': 'off',
      'jsdoc/require-returns-description': 'off',
      'jsdoc/require-returns-type': 'off',
      'jsdoc/require-returns': 'off',
      'jsdoc/tag-lines': [
        'warn',
        'never',
        {
          startLines: 1
        }
      ],

      // Automatically use template strings
      'no-useless-concat': 'error',
      'prefer-template': 'error',

      // Flow control
      'no-continue': 'error',
      'no-else-return': 'error',

      // Avoid hard to read multi assign statements
      'no-multi-assign': 'error',

      // Prefer rules that are type aware
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error'],
      '@stylistic/space-before-function-paren': 'off'
    },
    settings: {
      jsdoc: {
        mode: 'typescript'
      }
    }
  },

  // Browser JavaScript files
  {
    files: ['**/assets/js/**/*.{js,mjs}'],
    languageOptions: {
      globals: {
        HTMLElement: 'readonly',
        HTMLFormElement: 'readonly',
        HTMLButtonElement: 'readonly',
        HTMLDivElement: 'readonly',
        Element: 'readonly',
        Document: 'readonly',
        RequestInit: 'readonly',
        SubmitEvent: 'readonly'
      }
    },
    plugins: {
      jsdoc: jsdocPlugin
    },
    settings: {
      jsdoc: {
        mode: 'typescript'
      }
    }
  },

  // Jest setup files
  {
    files: ['jest.setup.js', '**/jest.setup.js'],
    extends: [jestPlugin.configs['flat/recommended']]
  },

  // CommonJS modules allow require statements
  {
    files: ['**/*.{cjs,js}'],
    rules: {
      '@typescript-eslint/no-require-imports': 'off',
      '@typescript-eslint/no-var-requires': 'off'
    }
  },

  // ES modules mandatory file extensions
  {
    files: ['**/*.mjs'],
    rules: {
      'import/extensions': [
        'error',
        'always',
        {
          ignorePackages: true,
          pattern: {
            cjs: 'always',
            js: 'always',
            mjs: 'always'
          }
        }
      ]
    }
  },

  // Jest test files
  {
    files: ['**/*.{test,spec}.{cjs,js,mjs}'],
    extends: [
      jestPlugin.configs['flat/recommended'],
      jestDomPlugin.configs['flat/recommended']
    ],
    rules: {
      '@typescript-eslint/no-empty-function': 'off',
      'promise/always-return': 'off',
      'promise/catch-or-return': 'off'
    }
  },

  // Configure ESLint in Markdown files
  {
    files: ['**/*.md'],
    plugins: {
      markdown: markdownPlugin
    },
    processor: 'markdown/markdown'
  },

  // Configure ESLint in Markdown code blocks
  {
    files: ['**/*.md/*.{cjs,js,mjs}'],
    rules: {
      '@typescript-eslint/no-unused-vars': 'off',
      'import/no-unresolved': 'off',
      'n/no-missing-import': 'off',
      'prefer-template': 'off'
    }
  }
)
