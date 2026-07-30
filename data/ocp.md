## Open/Closed Principle (OCP)

Software entities should be open for extension but closed for modification.

### Violating example

```typescript
class DiscountCalculator {
  calculate(type: string, price: number): number {
    if (type === "regular") return price;
    if (type === "vip") return price * 0.9;
    if (type === "employee") return price * 0.8;
    throw new Error("Unsupported discount type");
  }
}
```

Every time a new discount type is added, this class and its `if` chain must be modified, risking breaking existing logic.

### Compliant example

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

class EmployeeDiscount implements DiscountStrategy {
  apply(price: number): number {
    return price * 0.8;
  }
}

class DiscountCalculator {
  calculate(strategy: DiscountStrategy, price: number): number {
    return strategy.apply(price);
  }
}
```

To add a new discount, you create a new class implementing `DiscountStrategy`, without touching `DiscountCalculator`.