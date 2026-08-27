# Decorator Pattern

## Definition

The Decorator pattern attaches additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending behavior.

## Violating example

```typescript
class Coffee {
  cost(): number {
    return 5;
  }
}

class Latte extends Coffee {
  cost(): number {
    return super.cost() + 2;
  }
}

class ExtraMilk extends Coffee {
  cost(): number {
    return super.cost() + 1;
  }
}
```

This approach leads to many subclasses for every possible combination of toppings and behaviors. It is rigid and hard to maintain.

## Compliant example

```typescript
interface Coffee {
  cost(): number;
}

class SimpleCoffee implements Coffee {
  cost(): number {
    return 5;
  }
}

class CoffeeDecorator implements Coffee {
  constructor(protected component: Coffee) {}

  cost(): number {
    return this.component.cost();
  }
}

class MilkDecorator extends CoffeeDecorator {
  cost(): number {
    return super.cost() + 2;
  }
}

class VanillaDecorator extends CoffeeDecorator {
  cost(): number {
    return super.cost() + 3;
  }
}

const coffee = new VanillaDecorator(new MilkDecorator(new SimpleCoffee()));
console.log(coffee.cost());
```

Decorators let behavior be composed dynamically without creating a large inheritance tree.
