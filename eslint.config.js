import js from '@eslint/js'
import importPlugin from 'eslint-plugin-import'
import jestPlugin from 'eslint-plugin-jest'
import jestDomPlugin from 'eslint-plugin-jest-dom'
import jsdocPlugin from 'eslint-plugin-jsdoc'
import markdownPlugin from 'eslint-plugin-markdown'
import nPlugin from 'eslint-plugin-n'
import promisePlugin from 'eslint-plugin-promise'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  // Global ignores
  {
    ignores: [
      '**/compiled/**',
      '**/coverage/**',
      '**/staticfiles/**',
      'node_modules/**',
      'CHANGELOG.md'
    ]
  },

  // Base JavaScript configuration
  js.configs.recommended,

  // TypeScript configurations
  ...tseslint.configs.strict,
  ...tseslint.configs.stylistic,

  // Main configuration for JavaScript/TypeScript files
  {
    files: ['**/*.{cjs,js,mjs}'],
    plugins: {
      import: importPlugin,
      jsdoc: jsdocPlugin,
      n: nPlugin,
      promise: promisePlugin
    },
    rules: {
      // Import plugin rules
      'import/order': [
        'error',
        {
          alphabetize: { order: 'asc' },
          'newlines-between': 'always'
        }
      ],

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
      '@typescript-eslint/no-unused-vars': ['error']
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
        HTMLFormElement: 'readonly'
      }
    },
    plugins: {
      jsdoc: jsdocPlugin
    }
  },

  // Jest setup files
  {
    files: ['jest.setup.js', '**/jest.setup.js']
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

  // Configure ESLint in test files
  {
    files: [
      '**/*.test.{cjs,js,mjs}',
      'jest?(.*).config.*',
      'jest?(.*).setup.*'
    ],
    plugins: {
      jest: jestPlugin,
      'jest-dom': jestDomPlugin
    },
    languageOptions: {
      globals: {
        ...jestPlugin.environments.globals.globals
      }
    },
    rules: {
      ...jestPlugin.configs.recommended.rules,
      ...jestPlugin.configs.style.rules,
      ...jestDomPlugin.configs.recommended.rules,
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
    languageOptions: {
      globals: {
        window: 'readonly',
        document: 'readonly',
        console: 'readonly'
      }
    },
    rules: {
      '@typescript-eslint/no-unused-vars': 'off',
      'import/no-unresolved': 'off',
      'n/no-missing-import': 'off',
      'prefer-template': 'off'
    }
  }
)
