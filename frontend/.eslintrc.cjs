/**
 * TLDR; ESLint configuration for React project.
 * TODO: Add stricter rules and TypeScript config if you migrate.
 */

module.exports = {
  root: true,
  env: { browser: true, es2022: true },
  extends: ["eslint:recommended"],
  parserOptions: { ecmaVersion: "latest", sourceType: "module" },
  plugins: ["react", "react-hooks"],
  settings: { react: { version: "detect" } },
  rules: {
    "react/react-in-jsx-scope": "off",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
};

