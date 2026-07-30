## Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules; both should depend on abstractions.

### Violating example

```typescript
class MySQLDatabase {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL`);
  }
}

class UserService {
  private db = new MySQLDatabase();

  createUser(name: string): void {
    this.db.save(name);
  }
}
```

`UserService` (high-level) depends directly on `MySQLDatabase` (low-level). Switching databases forces changes to `UserService`.

### Compliant example

```typescript
interface Database {
  save(data: string): void;
}

class MySQLDatabase implements Database {
  save(data: string): void {
    console.log(`Saving "${data}" to MySQL`);
  }
}

class MongoDatabase implements Database {
  save(data: string): void {
    console.log(`Saving "${data}" to MongoDB`);
  }
}

class UserService {
  constructor(private db: Database) {}

  createUser(name: string): void {
    this.db.save(name);
  }
}

// Usage: the concrete implementation is injected from outside
const service = new UserService(new MongoDatabase());
```

`UserService` depends on the `Database` abstraction, not on a concrete implementation. Switching persistence engines doesn't require touching `UserService`.
