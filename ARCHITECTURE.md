# DataVisionX Architecture

Version: Phoenix 0.5

---

# System Layers

Application

↓

REST API

↓

Service Layer

↓

Runtime Registry

↓

Kernel

---

# Core

core/

kernel.py

runtime.py

bootstrap.py

daemon.py

config.py

logger.py

health.py

---

# Runtime

Runtime is responsible for:

- Service Registry
- Dependency Injection
- Runtime State
- Runtime Services

All services are registered once.

No duplicated services are allowed.

---

# Plugin System

Plugin Manager

↓

Loader

↓

Lifecycle

↓

Sandbox

↓

Storage

↓

Permissions

↓

Event Bus

---

# Rules

PluginManager must never create global services.

All shared services are requested from Runtime.

Every module has one responsibility.

---

# Future

Marketplace

Automation Studio

AI Center

Dashboard

Cluster

SDK

Mobile

Cloud

---

# Philosophy

Small kernel.

Everything else is modular.
