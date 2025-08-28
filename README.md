# ERPNext Engineering

ERPNext Engineering is a comprehensive engineering management module for ERPNext that provides advanced features for managing engineering projects, resources, technical documentation, and workflows.

## Features

- **Project Management**: Plan and track engineering projects with detailed task management
- **Resource Allocation**: Efficiently manage engineering resources and personnel
- **Technical Documentation**: Maintain engineering specifications, drawings, and documentation
- **Workflow Management**: Streamline engineering processes and approval workflows
- **Integration**: Seamless integration with ERPNext's manufacturing and project modules

## Installation

### Prerequisites

- Frappe Framework (>= 15.0.0)
- ERPNext (>= 15.0.0)
- Python (>= 3.10)

### Install via Bench

1. Get the app:
```bash
bench get-app https://github.com/teodoropiccinni/erpnext_engineering.git
```

2. Install the app on your site:
```bash
bench --site [sitename] install-app erpnext_engineering
```

3. Restart bench:
```bash
bench restart
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/teodoropiccinni/erpnext_engineering.git
```

2. Install in development mode:
```bash
bench get-app ./erpnext_engineering
bench --site [sitename] install-app erpnext_engineering
```

## Configuration

After installation, you can configure the Engineering module by:

1. Go to Setup > Engineering Settings
2. Configure default project types and engineering workflows
3. Set up engineering roles and permissions

## Usage

### Getting Started

1. Create Engineering Project Types
2. Set up Engineering Teams
3. Create your first Engineering Project
4. Add tasks and allocate resources

### Key Doctypes

- **Engineering Project**: Main project management doctype
- **Engineering Task**: Individual engineering tasks
- **Engineering Resource**: Resource management and allocation
- **Technical Document**: Engineering documentation and specifications

## Development

### Setting up for Development

1. Clone the repository
2. Create a new bench site
3. Install in development mode
4. Start development server

```bash
bench start
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact: teodoropiccinni@example.com

## Version

Current version: 1.0.0

---

Built with ❤️ for the ERPNext community