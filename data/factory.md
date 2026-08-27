# Factory Pattern

## Definition

The Factory pattern provides an interface for creating objects but allows subclasses to alter the type of objects that will be created. It encapsulates object creation logic.

## Violating example

```typescript
class MySQLDatabase {
  save(data: string): void {
    console.log(`Saving ${data} to MySQL`);
  }
}

class MongoDatabase {
  save(data: string): void {
    console.log(`Saving ${data} to MongoDB`);
  }
}

// Client decides which concrete to instantiate
const env = "mysql";
let db: any;
if (env === "mysql") db = new MySQLDatabase();
else db = new MongoDatabase();
```

This couples the client code to concrete classes and scatters creation logic.

## Compliant example

```typescript
interface Database {
  save(data: string): void;
}

class MySQLDatabase implements Database {
  save(data: string): void {
    console.log(`Saving ${data} to MySQL`);
  }
}

class MongoDatabase implements Database {
  save(data: string): void {
    console.log(`Saving ${data} to MongoDB`);
  }
}

class DatabaseFactory {
  static create(type: string): Database {
    if (type === "mysql") return new MySQLDatabase();
    return new MongoDatabase();
  }
}

const db = DatabaseFactory.create(process.env.DB_TYPE || "mysql");
db.save("payload");
```

Centralizing creation simplifies swapping implementations and testing.
