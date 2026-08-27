# Composite Pattern

## Definition
The Composite pattern composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly.

## Violating example
```typescript
class Employee {
  constructor(public name: string, public department: string) {}

  getTeamSize(): number {
    return 1;
  }
}

class Team {
  constructor(private members: Employee[]) {}

  getTeamSize(): number {
    return this.members.length;
  }
}
```
The client has to know whether it is dealing with a leaf or a composite object. This creates conditional logic and breaks uniform treatment.

## Compliant example
```typescript
interface EmployeeNode {
  getTeamSize(): number;
}

class Employee implements EmployeeNode {
  constructor(public name: string) {}

  getTeamSize(): number {
    return 1;
  }
}

class Team implements EmployeeNode {
  constructor(private members: EmployeeNode[]) {}

  getTeamSize(): number {
    return this.members.reduce((sum, member) => sum + member.getTeamSize(), 0);
  }
}

const team = new Team([
  new Employee("Ana"),
  new Team([
    new Employee("Luis"),
    new Employee("Marta")
  ])
]);

console.log(team.getTeamSize()); // 3
```
The Composite pattern allows the client to treat both individual and grouped objects uniformly.