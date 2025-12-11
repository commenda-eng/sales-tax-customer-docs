# Workflow Builder DSL types

## Expressions

It will evaluate to some value. ExpressionType will decide which engine will be used for evaluation. There can be different types of expressions but currently we only support JSONATA Expressions.

```ts
export enum ExpressionType {
  JSONATA = 'jsonata',
}export type TExpr = { type: ExpressionType.JSONATA; src: string };
```

### Evaluation Scope

This is not a type.

All the expressions are evaluated against an environment which is the Evaluation Scope. It has the following properties:.  
**“\_\_context\_\_”**  \- use this to access the global context.  
**“\_\_steps\_\_”**  \- use this to access any step’s output. Eg:- \_\_step\_\_.stepID.name  
**“\_\_datasources\_\_”**  \- use this to access any datasource’s output that was fetched during that step. Eg:- \_\_ds\_\_.dsID.corporation.companyLegalName  
**“\_\_each\_\_”**  \- use this to access each item when iterating through a collection. Eg:- \_\_each\_\_.id

## Value Providers

### TFieldRef

This defines how to access any field.  
Currently, there are 4 sources from where you can access the field which is defined using FieldRefSource.

* **FieldRefSource.CONTEXT** \- Access from the global context  
* **FieldRefSource.STEP** \- Access from the output of a step  
* **FieldRefSource.DATASOURCE** \- Access from the output of a datasource  
* **FieldRefSource.EACH** \- If you are within a loop, you can access individual item fields.

**path** \- It should be a **dot notation string** only. It will be used to access a particular key inside the source object. This is a string and not an expression. We are using a very light lib “dot-props” for it.

```ts
export type TFieldRef =
  | { source: FieldRefSource.CONTEXT; path: string }
  | { source: FieldRefSource.STEP; stepId: string; path: string }
  | { source: FieldRefSource.DATASOURCE; key: string; path: string }
  | { source: FieldRefSource.EACH; path: string }
```

### TValueProvider

Tell us how to produce a value. You produce a value in three ways :- 

- **const**: It is a hard coded value.   
- **field**: by accessing any field.  
- **expr**: computing an expression against the evaluation scope.

```ts
export type TValueProvider = 
| { type: "const"; value: unknown }
| { type: "field"; ref: TFieldRef } 
| { type: "expr"; expr: TExpr };
```

### TParamValue

This is used to generate the parameter values of a datasource or function which we would want to call.

```ts
export type TParamValue = TValueProvider | { [k: string]: TParamValue } | TParamValue[];
```

### TDatasourceCall

We have data sources in our system which you can call and fetch data. Sometimes we would want to use them within our workflow. You define a datasource call using TDatasourceCall.

```ts
export type TDataSourceCall = {
  id: string;
  alias: string;
  type: DataSourceType.COMMENDA_LOGICAL_BACKEND;
  dataSourceID: string; // from the db.
  params?: TParamValue;
  select?: TExpr; // Default - it will store the entire output of the data source. If you want to transform the output of the data source or store any specific field from the output.
  scope?: 'per-step' | 'per-item'; // default: per-step
};
```

### TIteratorProvider

These should output an array.  
**expression** \- it will evaluate the expression against the evaluation context.  
**step** \-  it will access the output of a step and return an array.  
**datasource** \- it will access the output of a data source and return an array. The datasource would be already loaded.

```ts
export type TIterableProvider =
  | { type: IterableType.EXPRESSION; expr: TExpr }
  | { type: IterableType.STEP; stepId: string; select?: TExpr }
  | { type: IterableType.DATASOURCE; key: string; select?: TExpr };
```

### TMapping

Each mapping specifies where the value should be written (targetPath) and how the value should be derived (value), along with an optional mode that controls how data is written.

* **targetPath** \- A dot-notation path (e.g., "director.id") representing where in the target object the value will be placed.  
* **mode** \- defines how the data should be written.  
  * **set** (default): replaces or sets the value at the target path.  
  * **append**: used when the target is an array; appends the new value.

	

```ts
export type TMapping = {
  id: string;
  targetPath: string;
  value: TValueProvider;
  mode?: 'set' | 'append';
};
```

Example :- 

```json
{
  "id": "map-directorId",
  "targetPath": "directorId",
  "value": {
    "type": "expr",
    "expr": { "src": "__each__.id" }
  },
  "mode": "set"
}
```

In the above example, directorId will be set to batch item id (`__each__.id).`