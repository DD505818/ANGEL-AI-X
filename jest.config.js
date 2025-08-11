module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  testMatch: ['**/web/src/tests/**/*.test.tsx'],
  moduleNameMapper: {
    '^web/(.*)$': '<rootDir>/web/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/web/src/tests/setup.ts'],
};
