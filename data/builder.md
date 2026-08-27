# Builder Pattern

## Definition

The Builder pattern separates the construction of a complex object from its representation, so the same construction process can create different representations.

## Violating example

```typescript
class User {
  name!: string;
  email!: string;
  age!: number;
  isAdmin!: boolean;

  constructor(name: string, email: string, age: number, isAdmin: boolean) {
    this.name = name;
    this.email = email;
    this.age = age;
    this.isAdmin = isAdmin;
  }
}

const user = new User("Ana", "ana@example.com", 30, false);
```

This constructor becomes hard to read and hard to extend as more optional fields are added. The object creation logic is cluttered and error-prone.

## Compliant example

```typescript
class User {
  name!: string;
  email!: string;
  age!: number;
  isAdmin = false;

  static builder() {
    return new UserBuilder();
  }
}

class UserBuilder {
  private user: User = new User();

  setName(name: string): UserBuilder {
    this.user.name = name;
    return this;
  }

  setEmail(email: string): UserBuilder {
    this.user.email = email;
    return this;
  }

  setAge(age: number): UserBuilder {
    this.user.age = age;
    return this;
  }

  setAdmin(isAdmin: boolean): UserBuilder {
    this.user.isAdmin = isAdmin;
    return this;
  }

  build(): User {
    return this.user;
  }
}

const user = User.builder()
  .setName("Ana")
  .setEmail("ana@example.com")
  .setAge(30)
  .setAdmin(false)
  .build();
```

The Builder keeps configuration readable and avoids a constructor with too many parameters.
