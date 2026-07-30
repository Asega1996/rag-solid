## Liskov Substitution Principle (LSP)

Objects of a derived class must be substitutable for objects of the base class without breaking the correctness of the program.

### Violating example

```typescript
class Bird {
  fly(): string {
    return "Flying";
  }
}

class Penguin extends Bird {
  fly(): string {
    throw new Error("Penguins can't fly");
  }
}

function makeBirdFly(bird: Bird): string {
  return bird.fly();
}

makeBirdFly(new Penguin()); // breaks at runtime
```

`Penguin` inherits from `Bird` but can't substitute it without breaking the expected contract (`fly()` always works).

### Compliant example

```typescript
interface Bird {
  move(): string;
}

interface FlyingBird extends Bird {
  fly(): string;
}

class Sparrow implements FlyingBird {
  move(): string {
    return "Flying";
  }
  fly(): string {
    return "Flying high";
  }
}

class Penguin implements Bird {
  move(): string {
    return "Swimming";
  }
}

function makeBirdMove(bird: Bird): string {
  return bird.move();
}
```

By separating flying capability into its own interface, any `Bird` can be substituted without breaking expected behavior.
