## Single Responsibility Principle (SRP)

A class should have only one reason to change. It should be responsible for a single piece of functionality.

### Violating example

```typescript
class Invoice {
  constructor(private items: { name: string; price: number }[]) {}

  calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  saveToDatabase(): void {
    // database connection and persistence logic
    console.log("Saving invoice to the database...");
  }

  printInvoice(): void {
    console.log(`Total: ${this.calculateTotal()}`);
  }
}
```

This class mixes three responsibilities: business calculation, persistence, and presentation. If the database engine or the print format changes, this same class has to be touched.

### Compliant example

```typescript
class Invoice {
  constructor(private items: { name: string; price: number }[]) {}

  calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

class InvoiceRepository {
  save(invoice: Invoice): void {
    console.log("Saving invoice to the database...");
  }
}

class InvoicePrinter {
  print(invoice: Invoice): void {
    console.log(`Total: ${invoice.calculateTotal()}`);
  }
}
```

Each class now has a single reason to change: `Invoice` if the business logic changes, `InvoiceRepository` if persistence changes, `InvoicePrinter` if the output format changes.
