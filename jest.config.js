/**
 * Jest config
 *
 * @type {Config}
 */
export default {
  collectCoverageFrom: ['**/assets/js/**/*.{js,mjs}'],
  coverageProvider: 'v8',
  // testMatch: ['<rootDir>/**/*.unit.test.{js,mjs}'],

  // Enable GitHub Actions reporter UI
  reporters: ['default', 'github-actions'],

  cacheDirectory: '<rootDir>/.cache/jest',
  coveragePathIgnorePatterns: ['.eslintrc.js', '.test.(js|mjs)'],

  // Enable Babel transforms until Jest supports ESM and `import()`
  // See: https://jestjs.io/docs/ecmascript-modules
  transform: {
    '^.+\\.(js|cjs)$': ['babel-jest', { rootMode: 'upward' }]
  },

  testEnvironment: 'jsdom',

  setupFilesAfterEnv: ['<rootDir>/jest-setup.js'],

  resetMocks: true,
  resetModules: true,
  restoreMocks: true,
  clearMocks: true
}

/**
 * @import { Config, ProjectConfig } from 'jest'
 */
