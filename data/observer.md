# Observer Pattern

## Definition

The Observer pattern defines a one-to-many dependency so that when one object changes state, its dependents are notified and updated automatically.

## Violating example

```typescript
class NewsPublisher {
  private subscribers: ((msg: string) => void)[] = [];

  subscribe(fn: (msg: string) => void) {
    this.subscribers.push(fn);
  }

  publish(msg: string) {
    // tightly coupled: logic to notify is mixed with business logic
    for (const s of this.subscribers) {
      s(msg);
    }
    console.log("Saved and notified");
  }
}
```

Publisher mixes notification and other responsibilities, and subscribers may be tightly coupled.

## Compliant example

```typescript
type Subscriber = (msg: string) => void;

class NewsPublisher {
  private subscribers: Subscriber[] = [];

  subscribe(fn: Subscriber) {
    this.subscribers.push(fn);
  }
  unsubscribe(fn: Subscriber) {
    this.subscribers = this.subscribers.filter((s) => s !== fn);
  }
  notify(msg: string) {
    this.subscribers.forEach((s) => s(msg));
  }

  publish(msg: string) {
    // single responsibility: persist then notify through a dedicated method
    this.save(msg);
    this.notify(msg);
  }

  private save(msg: string) {
    console.log("Saved:", msg);
  }
}

const pub = new NewsPublisher();
pub.subscribe((msg) => console.log("Listener A:", msg));
pub.publish("New article");
```

Separating concerns keeps responsibilities clear and allows loose coupling.
