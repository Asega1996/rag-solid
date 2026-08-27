# Singleton Pattern

## Definition

The Singleton pattern ensures that a class has only one instance and provides a global access point to it.

## Violating example

```typescript
class DatabaseConnection {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }
}

const connectionA = new DatabaseConnection("postgres://prod");
const connectionB = new DatabaseConnection("postgres://prod");
```

This creates multiple independent connection objects, which can lead to duplicated resources, inconsistent state, and unnecessary overhead.

## Compliant example

```typescript
class DatabaseConnection {
  private static instance: DatabaseConnection | null = null;
  private url: string;

  private constructor(url: string) {
    this.url = url;
  }

  static getInstance(url?: string): DatabaseConnection {
    if (!DatabaseConnection.instance) {
      if (!url) throw new Error("A URL is required for the first instance");
      DatabaseConnection.instance = new DatabaseConnection(url);
    }
    return DatabaseConnection.instance;
  }
}

const connectionA = DatabaseConnection.getInstance("postgres://prod");
const connectionB = DatabaseConnection.getInstance("postgres://prod");
console.log(connectionA === connectionB); // true
```

The Singleton guarantees a single instance, which is useful for shared resources such as configuration objects or connection pools.
