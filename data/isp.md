## Interface Segregation Principle (ISP)

No client should be forced to depend on methods it does not use. Prefer several small, specific interfaces over one large, general one.

### Violating example

```typescript
interface Worker {
  work(): void;
  eat(): void;
}

class RobotWorker implements Worker {
  work(): void {
    console.log("Working...");
  }
  eat(): void {
    throw new Error("A robot doesn't eat");
  }
}
```

`RobotWorker` is forced to implement `eat()`, a method that makes no sense for it.

### Compliant example

```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

class HumanWorker implements Workable, Eatable {
  work(): void {
    console.log("Working...");
  }
  eat(): void {
    console.log("Eating...");
  }
}

class RobotWorker implements Workable {
  work(): void {
    console.log("Working...");
  }
}
```

Each class implements only the interfaces it actually needs.
