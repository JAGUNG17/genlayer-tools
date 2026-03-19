# Contributing to GenLayer Tools & Infrastructure

We welcome and appreciate contributions from the community to make the GenLayer Tools & Infrastructure even better! Whether it's bug reports, feature requests, documentation improvements, or code contributions, your input is valuable.

## How to Contribute

### 1. Reporting Bugs

If you find a bug, please open an issue on our [GitHub Issues page](https://github.com/JAGUNG17/genlayer-tools/issues). When reporting a bug, please include:

-   A clear and concise description of the bug.
-   Steps to reproduce the behavior.
-   Expected behavior.
-   Screenshots or error messages if applicable.
-   Your GenLayer SDK version and Python version.

### 2. Suggesting Enhancements

We're always looking for ways to improve. If you have an idea for a new feature or an enhancement to an existing one, please open an issue on our [GitHub Issues page](https://github.com/JAGUNG17/genlayer-tools/issues) with the label `enhancement`. Describe your suggestion in detail and explain why it would be beneficial.

### 3. Code Contributions

We encourage you to contribute code! To do so, please follow these steps:

1.  **Fork the Repository**: Start by forking the `genlayer-tools` repository to your GitHub account.
2.  **Clone Your Fork**: Clone your forked repository to your local machine:
    ```bash
    git clone https://github.com/YOUR_USERNAME/genlayer-tools.git
    cd genlayer-tools
    ```
3.  **Create a New Branch**: Create a new branch for your feature or bug fix. Use a descriptive name (e.g., `feature/add-new-api`, `bugfix/weather-error-handling`).
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make Your Changes**: Implement your changes, ensuring you adhere to the existing coding style and add appropriate tests.
5.  **Test Your Changes**: Run existing tests and add new ones for your changes. Ensure all tests pass.
6.  **Update Documentation**: If your changes introduce new features or modify existing ones, update the relevant documentation files in the `docs/` directory and the `README.md`.
7.  **Commit Your Changes**: Write clear and concise commit messages.
    ```bash
    git commit -m "feat: Add new API integration for X"
    ```
8.  **Push to Your Fork**: Push your new branch to your forked repository on GitHub.
    ```bash
    git push origin feature/your-feature-name
    ```
9.  **Open a Pull Request**: Go to the original `genlayer-tools` repository on GitHub and open a new Pull Request from your forked branch. Provide a clear title and description of your changes.

## Coding Guidelines

-   **Pythonic Code**: Write clean, readable, and Pythonic code.
-   **Type Hinting**: Use Python type hints for better code clarity and maintainability.
-   **Error Handling**: Implement robust error handling for external API calls and other potential failure points.
-   **Equivalence Principle**: Ensure all external data fetches are wrapped with `gl.eq_principle.strict_eq` to maintain data integrity.
-   **Security**: Adhere to security best practices, especially regarding API key management.

Thank you for contributing to the GenLayer ecosystem!
