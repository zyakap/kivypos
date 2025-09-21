# StoaApp - Multi-Tenant POS SaaS Platform Architecture

## System Overview

**StoaApp** is a subscription-based SaaS platform that provides POS and inventory management solutions to trade store owners. Each trade store owner can manage multiple store locations, with each store having its own offline-capable POS system.

## Architecture Components

### 1. Backend SaaS Platform (Django + DRF)
- **Technology**: Python Django with Django REST Framework
- **Purpose**: Central platform management, subscription billing, multi-tenant data management
- **Location**: Cloud-hosted (online)
- **Database**: PostgreSQL with multi-tenant architecture

### 2. Store POS Client (Kivy)
- **Technology**: Python Kivy/KivyMD
- **Purpose**: Point-of-sale operations, inventory management, customer management
- **Location**: Store premises (offline-capable)
- **Database**: SQLite (local) with sync capabilities

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     StoaApp SaaS Platform                      │
│                   (Django + DRF Backend)                       │
├─────────────────────────────────────────────────────────────────┤
│  • Multi-tenant management                                     │
│  • Subscription & billing                                      │
│  • Trade store owner accounts                                  │
│  • Store configuration management                              │
│  • Central data synchronization                                │
│  • API endpoints for Kivy clients                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ API Communication
                                │ (REST API + Sync)
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    Store POS Clients                           │
│                     (Kivy Apps)                                │
├─────────────────────────────────────────────────────────────────┤
│  Store A          │  Store B          │  Store C               │
│  ┌─────────────┐  │  ┌─────────────┐  │  ┌─────────────┐      │
│  │ Kivy POS    │  │  │ Kivy POS    │  │  │ Kivy POS    │      │
│  │ SQLite DB   │  │  │ SQLite DB   │  │  │ SQLite DB   │      │
│  │ Offline     │  │  │ Offline     │  │  │ Offline     │      │
│  │ Capable     │  │  │ Capable     │  │  │ Capable     │      │
│  └─────────────┘  │  └─────────────┘  │  └─────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## User Hierarchy

1. **StoaApp Administrators** (Platform Level)
   - Manage platform settings
   - Set pricing models
   - Monitor system health
   - Handle billing and subscriptions

2. **Trade Store Owners** (Tenant Level)
   - Register and manage account
   - Add/remove store locations
   - Manage subscription and billing
   - Configure store settings
   - View consolidated reports

3. **Store Managers** (Store Level)
   - Manage store-specific settings
   - Oversee cashier accounts
   - Access store reports
   - Configure payment methods

4. **Cashiers** (Operational Level)
   - Process sales transactions
   - Manage inventory
   - Handle customer interactions
   - Generate receipts

## Database Architecture

### Backend (Django - PostgreSQL)

#### Multi-Tenant Tables:
- **tenants** - Trade store owner accounts
- **tenant_subscriptions** - Billing and subscription data
- **stores** - Store locations per tenant
- **store_settings** - Store-specific configurations
- **users** - All system users with tenant/store associations
- **sync_logs** - Data synchronization tracking

#### Synchronized Data Tables (per tenant):
- **products** - Product catalog
- **customers** - Customer database
- **sales** - Transaction records
- **inventory_movements** - Stock tracking
- **reports** - Generated reports

### Frontend (Kivy - SQLite)

#### Local Store Tables:
- **store_config** - Local store settings
- **users** - Local cashiers and managers
- **products** - Local product catalog (synced)
- **customers** - Local customer database (synced)
- **sales** - Local transaction records (synced)
- **inventory_movements** - Local stock tracking (synced)
- **sync_queue** - Pending sync operations

## Key Features

### SaaS Platform Features:
1. **Multi-Tenant Management**
   - Tenant isolation and data security
   - Subscription-based billing
   - Per-store pricing model
   - Automated invoicing

2. **Store Management**
   - Store registration and configuration
   - Payment method settings (DINAU/EFTPOS enable/disable)
   - User management per store
   - Centralized reporting

3. **API Services**
   - RESTful API for Kivy clients
   - Authentication and authorization
   - Data synchronization endpoints
   - Real-time configuration updates

### Kivy POS Features:
1. **Offline Operations**
   - Full POS functionality without internet
   - Local SQLite database
   - Queue-based sync when online

2. **POS Functionality**
   - Product search and barcode scanning
   - Shopping cart management
   - Multiple payment methods (Cash, EFTPOS, DINAU)
   - Receipt generation and printing

3. **Inventory Management**
   - Stock tracking and updates
   - Low stock alerts
   - Product management

4. **Customer Management**
   - Customer registration and search
   - Purchase history tracking

5. **Reporting**
   - Sales reports
   - Inventory reports
   - Export functionality

## Data Synchronization

### Sync Strategy:
1. **Bidirectional Sync**: Changes flow both ways between local and central databases
2. **Conflict Resolution**: Timestamp-based with manual resolution for conflicts
3. **Incremental Sync**: Only sync changed data since last sync
4. **Queue-Based**: Offline operations queued for sync when online

### Sync Triggers:
- Manual sync button in Kivy app
- Automatic sync when internet connection detected
- Scheduled sync intervals (configurable)
- Critical operations (end-of-day reports)

## Security & Compliance

1. **Multi-Tenant Data Isolation**
2. **API Authentication (JWT tokens)**
3. **Role-Based Access Control**
4. **Data Encryption (in transit and at rest)**
5. **Audit Logging**
6. **GDPR Compliance**

## Deployment Architecture

### Backend Deployment:
- **Cloud Provider**: AWS/GCP/Azure
- **Database**: Managed PostgreSQL
- **API**: Django application with Gunicorn/uWSGI
- **Web Server**: Nginx
- **Load Balancer**: Cloud load balancer
- **Monitoring**: Application monitoring and logging

### Kivy Client Deployment:
- **Distribution**: Executable packages for Windows/Mac/Linux
- **Updates**: Auto-update mechanism
- **Configuration**: Remote configuration management
- **Support**: Remote diagnostics and support tools

## Development Phases

### Phase 1: Backend SaaS Platform
1. Django project setup with multi-tenant architecture
2. User management and authentication
3. Tenant and store management
4. Subscription and billing system
5. API endpoints for Kivy clients

### Phase 2: Enhanced Kivy POS Client
1. Redesign for multi-tenant architecture
2. API integration and authentication
3. Data synchronization implementation
4. Offline capability enhancement
5. Store-specific configuration

### Phase 3: Advanced Features
1. Advanced reporting and analytics
2. Real-time notifications
3. Mobile companion apps
4. Third-party integrations
5. Advanced inventory features

## Technology Stack

### Backend:
- **Framework**: Django 4.x + Django REST Framework
- **Database**: PostgreSQL 14+
- **Authentication**: JWT + Django Auth
- **API Documentation**: Swagger/OpenAPI
- **Task Queue**: Celery + Redis
- **Caching**: Redis
- **File Storage**: AWS S3 or similar

### Frontend (Kivy):
- **Framework**: Kivy 2.x + KivyMD
- **Database**: SQLite 3
- **HTTP Client**: Requests library
- **Sync**: Custom sync engine
- **Packaging**: PyInstaller
- **Updates**: Custom update mechanism

### DevOps:
- **Containerization**: Docker
- **Orchestration**: Kubernetes or Docker Compose
- **CI/CD**: GitHub Actions or GitLab CI
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or similar
