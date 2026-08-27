# Adapter Pattern

## Definition

The Adapter pattern allows incompatible interfaces to work together by wrapping one interface in another that clients expect. It promotes interoperability without changing existing code.

## Violating example

```typescript
class PaymentGateway {
  processPayment(amount: number): void {
    console.log(`Processing payment of ${amount}`);
  }
}

class CheckoutService {
  private gateway: PaymentGateway;

  constructor() {
    this.gateway = new PaymentGateway();
  }

  pay(amount: number): void {
    this.gateway.processPayment(amount);
  }
}
```

This works only while the dependency matches the expected interface exactly. If a new payment provider exposes a different API, the `CheckoutService` must change.

## Compliant example

```typescript
interface PaymentProvider {
  charge(amount: number): void;
}

class StripeGateway implements PaymentProvider {
  charge(amount: number): void {
    console.log(`Charging ${amount} through Stripe`);
  }
}

class LegacyPaymentGateway {
  processPayment(amount: number): void {
    console.log(`Processing payment of ${amount} with legacy provider`);
  }
}

class LegacyAdapter implements PaymentProvider {
  constructor(private legacy: LegacyPaymentGateway) {}

  charge(amount: number): void {
    this.legacy.processPayment(amount);
  }
}

class CheckoutService {
  constructor(private provider: PaymentProvider) {}

  pay(amount: number): void {
    this.provider.charge(amount);
  }
}

const service = new CheckoutService(
  new LegacyAdapter(new LegacyPaymentGateway()),
);
service.pay(100);
```

The Adapter lets existing components work with new interfaces without forcing invasive code changes.
