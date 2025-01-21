# tenant_assignment
# Django Tenant Project

## Setup Instructions

### Prerequisites
- **Python 3.8+**: Ensure Python 3.8 or above is installed.
- **PostgreSQL**: A PostgreSQL database is required for multi-tenancy and tenant schema management.
- **Elasticsearch**: Elasticsearch should be installed and running for indexing and searching blog posts.
- **Django 3.x+**: The application is built using Django 3.x or higher.

### Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Database
Ensure the PostgreSQL database is set up and properly configured in your Django settings.

---

## How Users Will Interact with the Application

### Superadmin Access

#### Login as Superadmin:
- A superadmin logs into the Django admin interface, typically at `/admin/`.

#### Create a New Client (Tenant):
1. Navigate to the **Client model** (`myapp.Client`) in the Django Admin panel.
2. Provide the necessary details such as:
   - **Tenant Name** (e.g., `tenant1`)
   - **Schema Name** (e.g., `tenant1_schema`)

This creates a new tenant entry in the **Client** model, linked to a new schema in the PostgreSQL database.

#### Associating a Domain with the Tenant
1. **Create a Domain for the Tenant**:
   - Navigate to the **Domain model** and associate a domain with the newly created tenant.
   - Example: For `tenant1`, create a domain such as `tenant1.com` linked to the tenant’s schema (`tenant1_schema`).

2. **Configure Domain in the System**:
   - Ensure the domain (e.g., `tenant1.com`) is correctly pointing to the tenant’s schema in the database.

Example:
```python
public_client = Client.objects.create(
    schema_name='public',
    name='Public Tenant',
)

Domain.objects.create(
    domain='127.0.0.1',
    tenant=public_client
)
```

---

### User Registration for a Specific Tenant (Domain)

1. **Access the Tenant’s Domain**:
   - A user navigates to the domain associated with the tenant (e.g., `tenant1.com`).
   - The application detects the active schema corresponding to the domain, ensuring tenant-specific data is shown.

2. **Registration Process**:
   - On `tenant1.com`, a registration page (e.g., `/register/`) is available for new users.
   - The registration page is tailored for the tenant (e.g., `tenant1`), ensuring users are associated with the correct schema.

3. **Registration Flow**:
   1. The user visits the registration page of `tenant1.com`.
   2. The user fills out a registration form with details such as name, email, and password.
   3. Upon form submission, the user is created within the tenant’s schema (e.g., `tenant1_schema`).
   4. A new user entry is created in the database.

---

### Tenant-Specific Blog Post Functionality

1. **Access Blog Posts**:
   - Registered users can view, create, and interact with blog posts specific to their tenant.
   - Blog posts are stored in the database within the tenant’s schema.

2. **Isolation of Blog Posts**:
   - Blog posts created by a tenant are isolated from other tenants, even though they share the same application code.

3. **Example**:
   - When a user accesses the blog section on `tenant1.com`, only `tenant1`’s blog posts are shown.

4. **Creating Blog Posts**:
   - Users with the proper permissions can create new blog posts.
   - These posts are associated with the tenant’s schema and visible only to users of that tenant.

---

## Example Workflow for Superadmin
1. Login to `/admin/` as a superadmin.
2. Create a new tenant by providing a **Tenant Name** and **Schema Name**.
3. Associate a domain with the tenant.
4. Verify the domain is pointing to the correct schema.

---

## Example Workflow for Tenant Users
1. Access the tenant’s domain (e.g., `tenant1.com`).
2. Register through the tenant-specific registration page.
3. Log in to view and interact with tenant-specific blog posts.
4. Create new blog posts if permissions allow.
