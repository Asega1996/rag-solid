# Strategy Pattern

## Definition

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

## Violating example

```typescript
class DiscountCalculator {
  calculate(type: string, price: number): number {
    if (type === "regular") return price;
    if (type === "vip") return price * 0.9;
    if (type === "employee") return price * 0.8;
    throw new Error("Unsupported discount type");
  }
}

const calc = new DiscountCalculator();
console.log(calc.calculate("vip", 100));
```

This implementation violates the Open/Closed Principle because adding a new discount type requires modifying `DiscountCalculator`.

## Compliant example

```typescript
interface DiscountStrategy {
  apply(price: number): number;
}

class RegularDiscount implements DiscountStrategy {
  apply(price: number): number {
    return price;
  }
}

class VipDiscount implements DiscountStrategy {
  apply(price: number): number {
    return price * 0.9;
  }
}

class DiscountCalculator {
  constructor(private strategy: DiscountStrategy) {}
  calculate(price: number): number {
    return this.strategy.apply(price);
  }
}

const calc = new DiscountCalculator(new VipDiscount());
console.log(calc.calculate(100));
```

Using `DiscountStrategy` allows adding new behaviors without modifying `DiscountCalculator`.
