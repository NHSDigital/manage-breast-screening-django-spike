import { defineConfig, globalIgnores } from 'eslint/config'
import neostandard from 'neostandard'
import pluginJest from 'eslint-plugin-jest'
import pluginJestDom from 'eslint-plugin-jest-dom'
import globals from 'globals'

export default defineConfig([
  globalIgnores([
    '**/compiled/**',
    '**/coverage/**',
    '**/staticfiles/**',

    // Enable dotfile linting
    '!.*',
    'node_modules',
    'node_modules/.*',

    // Prevent CHANGELOG history changes
    'CHANGELOG.md'
  ]),

  neostandard({
    files: ['**/*.{cjs,js,mjs}']
  }),

  // Configure ESLint in test files
  {
    files: [
      '**/*.test.{cjs,js,mjs}',
      'jest?(.*).config.*',
      'jest?(.*).setup.*'
    ],
    extends: [
      pluginJest.configs['flat/recommended'],
      pluginJest.configs['flat/style'],
      pluginJestDom.configs['flat/recommended']
    ],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...pluginJest.environments.globals.globals
      }
    },
    rules: {
      '@typescript-eslint/no-empty-function': 'off',
      'promise/always-return': 'off',
      'promise/catch-or-return': 'off'
    }
  }
])

/**
 * @import { ConfigWithExtends } from '@eslint/config-helpers'
 * @import { Linter } from 'eslint'
 */
