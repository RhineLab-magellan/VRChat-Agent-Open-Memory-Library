# 已暴露类型详细清单 - VRChat SDK 3.10.3

> Type: REFERENCE
> Source: `参考文献/UdonTypeExposure.txt` 解析
> SDK Version: 3.10.3
> Confidence: High
> Last Updated: 2026-06-11

---

## 概述

- 总类型数：1387
- 有暴露成员的类型：1067
- 暴露成员总数：9579
- 未暴露成员总数：6323

---

## UnityEngine 核心类型

### GameObject
- 暴露率: 50.0%
- 暴露成员: 35
- 完整名称: `Playables.GameObject`

**方法：**
- `T GetComponent[T]()`
- `UnityEngine.Component GetComponent(System.Type)`
- `UnityEngine.Component GetComponent(System.String)`
- `UnityEngine.Component GetComponentInChildren(System.Type, Boolean)`
- `UnityEngine.Component GetComponentInChildren(System.Type)`
- `T GetComponentInChildren[T]()`
- `T GetComponentInChildren[T](Boolean)`
- `UnityEngine.Component GetComponentInParent(System.Type, Boolean)`
- `UnityEngine.Component GetComponentInParent(System.Type)`
- `T GetComponentInParent[T]()`
- `T GetComponentInParent[T](Boolean)`
- `UnityEngine.Component[] GetComponents(System.Type)`
- `T[] GetComponents[T]()`
- `Void GetComponents(System.Type, System.Collections.Generic.List`1[UnityEngine.Component])`
- `Void GetComponents[T](System.Collections.Generic.List`1[T])`
- ... 等 13 个方法

**属性/字段：**
- `UnityEngine.Transform transform`
- `Int32 layer`
- `Boolean activeSelf`
- `Boolean activeInHierarchy`
- `Boolean isStatic`
- `UnityEngine.GameObject gameObject`

### Transform
- 暴露率: 84.21%
- 暴露成员: 64
- 完整名称: `Playables.Transform`

**方法：**
- `Void SetParent(UnityEngine.Transform)`
- `Void SetParent(UnityEngine.Transform, Boolean)`
- `Void SetPositionAndRotation(UnityEngine.Vector3, UnityEngine.Quaternion)`
- `Void SetLocalPositionAndRotation(UnityEngine.Vector3, UnityEngine.Quaternion)`
- `Void GetPositionAndRotation(UnityEngine.Vector3 ByRef, UnityEngine.Quaternion ByRef)`
- `Void GetLocalPositionAndRotation(UnityEngine.Vector3 ByRef, UnityEngine.Quaternion ByRef)`
- `Void Translate(UnityEngine.Vector3, UnityEngine.Space)`
- `Void Translate(UnityEngine.Vector3)`
- `Void Translate(Single, Single, Single, UnityEngine.Space)`
- `Void Translate(Single, Single, Single)`
- `Void Translate(UnityEngine.Vector3, UnityEngine.Transform)`
- `Void Translate(Single, Single, Single, UnityEngine.Transform)`
- `Void Rotate(UnityEngine.Vector3, UnityEngine.Space)`
- `Void Rotate(UnityEngine.Vector3)`
- `Void Rotate(Single, Single, Single, UnityEngine.Space)`
- ... 等 29 个方法

**属性/字段：**
- `UnityEngine.Vector3 position`
- `UnityEngine.Vector3 localPosition`
- `UnityEngine.Vector3 eulerAngles`
- `UnityEngine.Vector3 localEulerAngles`
- `UnityEngine.Vector3 right`
- `UnityEngine.Vector3 up`
- `UnityEngine.Vector3 forward`
- `UnityEngine.Quaternion rotation`
- `UnityEngine.Quaternion localRotation`
- `UnityEngine.Vector3 localScale`
- `UnityEngine.Transform parent`
- `UnityEngine.Matrix4x4 worldToLocalMatrix`
- `UnityEngine.Matrix4x4 localToWorldMatrix`
- `UnityEngine.Transform root`
- `Int32 childCount`
- `UnityEngine.Vector3 lossyScale`
- `Boolean hasChanged`
- `Int32 hierarchyCapacity`
- `Int32 hierarchyCount`

### Component
- 暴露率: 61.7%
- 暴露成员: 29
- 完整名称: `Playables.Component`

**方法：**
- `UnityEngine.Component GetComponent(System.Type)`
- `T GetComponent[T]()`
- `UnityEngine.Component GetComponent(System.String)`
- `UnityEngine.Component GetComponentInChildren(System.Type, Boolean)`
- `UnityEngine.Component GetComponentInChildren(System.Type)`
- `T GetComponentInChildren[T](Boolean)`
- `T GetComponentInChildren[T]()`
- `UnityEngine.Component[] GetComponentsInChildren(System.Type, Boolean)`
- `UnityEngine.Component[] GetComponentsInChildren(System.Type)`
- `T[] GetComponentsInChildren[T](Boolean)`
- `Void GetComponentsInChildren[T](Boolean, System.Collections.Generic.List`1[T])`
- `T[] GetComponentsInChildren[T]()`
- `Void GetComponentsInChildren[T](System.Collections.Generic.List`1[T])`
- `UnityEngine.Component GetComponentInParent(System.Type, Boolean)`
- `UnityEngine.Component GetComponentInParent(System.Type)`
- ... 等 11 个方法

**属性/字段：**
- `UnityEngine.Transform transform`
- `UnityEngine.GameObject gameObject`

### Object
- 暴露率: 100.0%
- 暴露成员: 8
- 完整名称: `Diagnostics.Object`

**方法：**
- `Boolean Equals(System.Object)`
- `<Static> Boolean Equals(System.Object, System.Object)`
- `Int32 GetHashCode()`
- `System.Type GetType()`
- `System.String ToString()`
- `<Static> Boolean ReferenceEquals(System.Object, System.Object)`

### Vector3
- 暴露率: 100.0%
- 暴露成员: 65
- 完整名称: `Playables.Vector3`

**方法：**
- `<Static> UnityEngine.Vector3 Slerp(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> UnityEngine.Vector3 SlerpUnclamped(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> Void OrthoNormalize(UnityEngine.Vector3 ByRef, UnityEngine.Vector3 ByRef)`
- `<Static> Void OrthoNormalize(UnityEngine.Vector3 ByRef, UnityEngine.Vector3 ByRef, UnityEngine.Vector3 ByRef)`
- `<Static> UnityEngine.Vector3 RotateTowards(UnityEngine.Vector3, UnityEngine.Vector3, Single, Single)`
- `<Static> UnityEngine.Vector3 Lerp(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> UnityEngine.Vector3 LerpUnclamped(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> UnityEngine.Vector3 MoveTowards(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> UnityEngine.Vector3 SmoothDamp(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.Vector3 ByRef, Single, Single)`
- `<Static> UnityEngine.Vector3 SmoothDamp(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.Vector3 ByRef, Single)`
- `<Static> UnityEngine.Vector3 SmoothDamp(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.Vector3 ByRef, Single, Single, Single)`
- `Void Set(Single, Single, Single)`
- `<Static> UnityEngine.Vector3 Scale(UnityEngine.Vector3, UnityEngine.Vector3)`
- `Void Scale(UnityEngine.Vector3)`
- `<Static> UnityEngine.Vector3 Cross(UnityEngine.Vector3, UnityEngine.Vector3)`
- ... 等 28 个方法

**属性/字段：**
- `<Static> System.Single kEpsilon`
- `<Static> System.Single kEpsilonNormalSqrt`
- `System.Single x`
- `System.Single y`
- `System.Single z`
- `Single Item [Int32]`
- `UnityEngine.Vector3 normalized`
- `Single magnitude`
- `Single sqrMagnitude`
- `<Static> UnityEngine.Vector3 zero`
- `<Static> UnityEngine.Vector3 one`
- `<Static> UnityEngine.Vector3 forward`
- `<Static> UnityEngine.Vector3 back`
- `<Static> UnityEngine.Vector3 up`
- `<Static> UnityEngine.Vector3 down`
- `<Static> UnityEngine.Vector3 left`
- `<Static> UnityEngine.Vector3 right`
- `<Static> UnityEngine.Vector3 positiveInfinity`
- `<Static> UnityEngine.Vector3 negativeInfinity`

### Vector2
- 暴露率: 100.0%
- 暴露成员: 57
- 完整名称: `Playables.Vector2`

**方法：**
- `Void Set(Single, Single)`
- `<Static> UnityEngine.Vector2 Lerp(UnityEngine.Vector2, UnityEngine.Vector2, Single)`
- `<Static> UnityEngine.Vector2 LerpUnclamped(UnityEngine.Vector2, UnityEngine.Vector2, Single)`
- `<Static> UnityEngine.Vector2 MoveTowards(UnityEngine.Vector2, UnityEngine.Vector2, Single)`
- `<Static> UnityEngine.Vector2 Scale(UnityEngine.Vector2, UnityEngine.Vector2)`
- `Void Scale(UnityEngine.Vector2)`
- `Void Normalize()`
- `System.String ToString()`
- `System.String ToString(System.String)`
- `System.String ToString(System.String, System.IFormatProvider)`
- `Int32 GetHashCode()`
- `Boolean Equals(System.Object)`
- `Boolean Equals(UnityEngine.Vector2)`
- `<Static> UnityEngine.Vector2 Reflect(UnityEngine.Vector2, UnityEngine.Vector2)`
- `<Static> UnityEngine.Vector2 Perpendicular(UnityEngine.Vector2)`
- ... 等 24 个方法

**属性/字段：**
- `System.Single x`
- `System.Single y`
- `<Static> System.Single kEpsilon`
- `<Static> System.Single kEpsilonNormalSqrt`
- `Single Item [Int32]`
- `UnityEngine.Vector2 normalized`
- `Single magnitude`
- `Single sqrMagnitude`
- `<Static> UnityEngine.Vector2 zero`
- `<Static> UnityEngine.Vector2 one`
- `<Static> UnityEngine.Vector2 up`
- `<Static> UnityEngine.Vector2 down`
- `<Static> UnityEngine.Vector2 left`
- `<Static> UnityEngine.Vector2 right`
- `<Static> UnityEngine.Vector2 positiveInfinity`
- `<Static> UnityEngine.Vector2 negativeInfinity`

### Quaternion
- 暴露率: 100.0%
- 暴露成员: 42
- 完整名称: `Playables.Quaternion`

**方法：**
- `<Static> UnityEngine.Quaternion FromToRotation(UnityEngine.Vector3, UnityEngine.Vector3)`
- `<Static> UnityEngine.Quaternion Inverse(UnityEngine.Quaternion)`
- `<Static> UnityEngine.Quaternion Slerp(UnityEngine.Quaternion, UnityEngine.Quaternion, Single)`
- `<Static> UnityEngine.Quaternion SlerpUnclamped(UnityEngine.Quaternion, UnityEngine.Quaternion, Single)`
- `<Static> UnityEngine.Quaternion Lerp(UnityEngine.Quaternion, UnityEngine.Quaternion, Single)`
- `<Static> UnityEngine.Quaternion LerpUnclamped(UnityEngine.Quaternion, UnityEngine.Quaternion, Single)`
- `<Static> UnityEngine.Quaternion AngleAxis(Single, UnityEngine.Vector3)`
- `<Static> UnityEngine.Quaternion LookRotation(UnityEngine.Vector3, UnityEngine.Vector3)`
- `<Static> UnityEngine.Quaternion LookRotation(UnityEngine.Vector3)`
- `Void Set(Single, Single, Single, Single)`
- `<Static> UnityEngine.Quaternion op_Multiply(UnityEngine.Quaternion, UnityEngine.Quaternion)`
- `<Static> UnityEngine.Vector3 op_Multiply(UnityEngine.Quaternion, UnityEngine.Vector3)`
- `<Static> Boolean op_Equality(UnityEngine.Quaternion, UnityEngine.Quaternion)`
- `<Static> Boolean op_Inequality(UnityEngine.Quaternion, UnityEngine.Quaternion)`
- `<Static> Single Dot(UnityEngine.Quaternion, UnityEngine.Quaternion)`
- ... 等 16 个方法

**属性/字段：**
- `System.Single x`
- `System.Single y`
- `System.Single z`
- `System.Single w`
- `<Static> System.Single kEpsilon`
- `Single Item [Int32]`
- `<Static> UnityEngine.Quaternion identity`
- `UnityEngine.Vector3 eulerAngles`
- `UnityEngine.Quaternion normalized`

### Time
- 暴露率: 77.78%
- 暴露成员: 21
- 完整名称: `Playables.Time`

**属性/字段：**
- `<Static> Single time`
- `<Static> Double timeAsDouble`
- `<Static> Single timeSinceLevelLoad`
- `<Static> Double timeSinceLevelLoadAsDouble`
- `<Static> Single deltaTime`
- `<Static> Single fixedTime`
- `<Static> Double fixedTimeAsDouble`
- `<Static> Single unscaledTime`
- `<Static> Double unscaledTimeAsDouble`
- `<Static> Single fixedUnscaledTime`
- `<Static> Double fixedUnscaledTimeAsDouble`
- `<Static> Single unscaledDeltaTime`
- `<Static> Single fixedUnscaledDeltaTime`
- `<Static> Single fixedDeltaTime`
- `<Static> Single smoothDeltaTime`
- `<Static> Int32 frameCount`
- `<Static> Int32 renderedFrameCount`
- `<Static> Single realtimeSinceStartup`
- `<Static> Double realtimeSinceStartupAsDouble`
- `<Static> Boolean inFixedTimeStep`

### Mathf
- 暴露率: 100.0%
- 暴露成员: 68
- 完整名称: `Playables.Mathf`

**方法：**
- `<Static> Int32 ClosestPowerOfTwo(Int32)`
- `<Static> Boolean IsPowerOfTwo(Int32)`
- `<Static> Int32 NextPowerOfTwo(Int32)`
- `<Static> Single GammaToLinearSpace(Single)`
- `<Static> Single LinearToGammaSpace(Single)`
- `<Static> UnityEngine.Color CorrelatedColorTemperatureToRGB(Single)`
- `<Static> UInt16 FloatToHalf(Single)`
- `<Static> Single HalfToFloat(UInt16)`
- `<Static> Single PerlinNoise(Single, Single)`
- `<Static> Single PerlinNoise1D(Single)`
- `<Static> Single Sin(Single)`
- `<Static> Single Cos(Single)`
- `<Static> Single Tan(Single)`
- `<Static> Single Asin(Single)`
- `<Static> Single Acos(Single)`
- ... 等 46 个方法

**属性/字段：**
- `<Static> System.Single PI`
- `<Static> System.Single Infinity`
- `<Static> System.Single NegativeInfinity`
- `<Static> System.Single Deg2Rad`
- `<Static> System.Single Rad2Deg`
- `<Static> System.Single Epsilon`

### Color
- 暴露率: 100.0%
- 暴露成员: 44
- 完整名称: `Playables.Color`

**方法：**
- `System.String ToString()`
- `System.String ToString(System.String)`
- `System.String ToString(System.String, System.IFormatProvider)`
- `Int32 GetHashCode()`
- `Boolean Equals(System.Object)`
- `Boolean Equals(UnityEngine.Color)`
- `<Static> UnityEngine.Color op_Addition(UnityEngine.Color, UnityEngine.Color)`
- `<Static> UnityEngine.Color op_Subtraction(UnityEngine.Color, UnityEngine.Color)`
- `<Static> UnityEngine.Color op_Multiply(UnityEngine.Color, UnityEngine.Color)`
- `<Static> UnityEngine.Color op_Multiply(UnityEngine.Color, Single)`
- `<Static> UnityEngine.Color op_Multiply(Single, UnityEngine.Color)`
- `<Static> UnityEngine.Color op_Division(UnityEngine.Color, Single)`
- `<Static> Boolean op_Equality(UnityEngine.Color, UnityEngine.Color)`
- `<Static> Boolean op_Inequality(UnityEngine.Color, UnityEngine.Color)`
- `<Static> UnityEngine.Color Lerp(UnityEngine.Color, UnityEngine.Color, Single)`
- ... 等 6 个方法

**属性/字段：**
- `System.Single r`
- `System.Single g`
- `System.Single b`
- `System.Single a`
- `<Static> UnityEngine.Color red`
- `<Static> UnityEngine.Color green`
- `<Static> UnityEngine.Color blue`
- `<Static> UnityEngine.Color white`
- `<Static> UnityEngine.Color black`
- `<Static> UnityEngine.Color yellow`
- `<Static> UnityEngine.Color cyan`
- `<Static> UnityEngine.Color magenta`
- `<Static> UnityEngine.Color gray`
- `<Static> UnityEngine.Color grey`
- `<Static> UnityEngine.Color clear`
- `Single grayscale`
- `UnityEngine.Color linear`
- `UnityEngine.Color gamma`
- `Single maxColorComponent`
- `Single Item [Int32]`

### Bounds
- 暴露率: 100.0%
- 暴露成员: 26
- 完整名称: `Playables.Bounds`

**方法：**
- `Int32 GetHashCode()`
- `Boolean Equals(System.Object)`
- `Boolean Equals(UnityEngine.Bounds)`
- `<Static> Boolean op_Equality(UnityEngine.Bounds, UnityEngine.Bounds)`
- `<Static> Boolean op_Inequality(UnityEngine.Bounds, UnityEngine.Bounds)`
- `Void SetMinMax(UnityEngine.Vector3, UnityEngine.Vector3)`
- `Void Encapsulate(UnityEngine.Vector3)`
- `Void Encapsulate(UnityEngine.Bounds)`
- `Void Expand(Single)`
- `Void Expand(UnityEngine.Vector3)`
- `Boolean Intersects(UnityEngine.Bounds)`
- `Boolean IntersectRay(UnityEngine.Ray)`
- `Boolean IntersectRay(UnityEngine.Ray, Single ByRef)`
- `System.String ToString()`
- `System.String ToString(System.String)`
- ... 等 4 个方法

**属性/字段：**
- `UnityEngine.Vector3 center`
- `UnityEngine.Vector3 size`
- `UnityEngine.Vector3 extents`
- `UnityEngine.Vector3 min`
- `UnityEngine.Vector3 max`

### LayerMask
- 暴露率: 100.0%
- 暴露成员: 7
- 完整名称: `Playables.LayerMask`

**方法：**
- `<Static> Int32 op_Implicit(UnityEngine.LayerMask)`
- `<Static> UnityEngine.LayerMask op_Implicit(Int32)`
- `<Static> System.String LayerToName(Int32)`
- `<Static> Int32 NameToLayer(System.String)`
- `<Static> Int32 GetMask(System.String[])`

**属性/字段：**
- `Int32 value`

### KeyCode
- 暴露率: 100.0%
- 暴露成员: 1
- 完整名称: `Playables.KeyCode`

### Input
- 暴露率: 40.38%
- 暴露成员: 21
- 完整名称: `Playables.Input`

**方法：**
- `<Static> Single GetAxis(System.String)`
- `<Static> Single GetAxisRaw(System.String)`
- `<Static> Boolean GetButton(System.String)`
- `<Static> Boolean GetButtonDown(System.String)`
- `<Static> Boolean GetButtonUp(System.String)`
- `<Static> Boolean GetMouseButton(Int32)`
- `<Static> Boolean GetMouseButtonDown(Int32)`
- `<Static> Boolean GetMouseButtonUp(Int32)`
- `<Static> System.String[] GetJoystickNames()`
- `<Static> Boolean GetKey(UnityEngine.KeyCode)`
- `<Static> Boolean GetKey(System.String)`
- `<Static> Boolean GetKeyUp(UnityEngine.KeyCode)`
- `<Static> Boolean GetKeyUp(System.String)`
- `<Static> Boolean GetKeyDown(UnityEngine.KeyCode)`
- `<Static> Boolean GetKeyDown(System.String)`

**属性/字段：**
- `<Static> Boolean anyKey`
- `<Static> Boolean anyKeyDown`
- `<Static> System.String inputString`
- `<Static> Boolean imeIsSelected`

## 物理系统

### Rigidbody
- 暴露率: 97.26%
- 暴露成员: 71
- 完整名称: `Playables.Rigidbody`

**方法：**
- `Void SetDensity(Single)`
- `Void MovePosition(UnityEngine.Vector3)`
- `Void MoveRotation(UnityEngine.Quaternion)`
- `Void Move(UnityEngine.Vector3, UnityEngine.Quaternion)`
- `Void Sleep()`
- `Boolean IsSleeping()`
- `Void WakeUp()`
- `Void ResetCenterOfMass()`
- `Void ResetInertiaTensor()`
- `UnityEngine.Vector3 GetRelativePointVelocity(UnityEngine.Vector3)`
- `UnityEngine.Vector3 GetPointVelocity(UnityEngine.Vector3)`
- `UnityEngine.Vector3 GetAccumulatedForce(Single)`
- ... 等 31 个方法

**属性/字段：**
- `UnityEngine.Vector3 velocity`
- `UnityEngine.Vector3 angularVelocity`
- `Single drag`
- `Single angularDrag`
- `Single mass`
- `Boolean useGravity`
- `Single maxDepenetrationVelocity`
- `Boolean isKinematic`
- `Boolean freezeRotation`
- `UnityEngine.RigidbodyConstraints constraints`
- `UnityEngine.CollisionDetectionMode collisionDetectionMode`
- `Boolean automaticCenterOfMass`
- `UnityEngine.Vector3 centerOfMass`
- `UnityEngine.Vector3 worldCenterOfMass`
- `Boolean automaticInertiaTensor`
- ... 等 12 个属性

### Rigidbody2D
- 暴露率: 98.73%
- 暴露成员: 78
- 完整名称: `Playables.Rigidbody2D`

**方法：**
- `Void SetRotation(Single)`
- `Void SetRotation(UnityEngine.Quaternion)`
- `Void MovePosition(UnityEngine.Vector2)`
- `Void MoveRotation(Single)`
- `Void MoveRotation(UnityEngine.Quaternion)`
- `Boolean IsSleeping()`
- `Boolean IsAwake()`
- `Void Sleep()`
- `Void WakeUp()`
- `Boolean IsTouching(UnityEngine.Collider2D)`
- `Boolean IsTouching(UnityEngine.Collider2D, UnityEngine.ContactFilter2D)`
- `Boolean IsTouching(UnityEngine.ContactFilter2D)`
- ... 等 38 个方法

**属性/字段：**
- `UnityEngine.Vector2 position`
- `Single rotation`
- `UnityEngine.Vector2 velocity`
- `Single angularVelocity`
- `Boolean useAutoMass`
- `Single mass`
- `UnityEngine.PhysicsMaterial2D sharedMaterial`
- `UnityEngine.Vector2 centerOfMass`
- `UnityEngine.Vector2 worldCenterOfMass`
- `Single inertia`
- `Single drag`
- `Single angularDrag`
- `Single gravityScale`
- `UnityEngine.RigidbodyType2D bodyType`
- `Boolean useFullKinematicContacts`
- ... 等 12 个属性

### Collider
- 暴露率: 94.44%
- 暴露成员: 17
- 完整名称: `Playables.Collider`

**方法：**
- `UnityEngine.Vector3 ClosestPoint(UnityEngine.Vector3)`
- `Boolean Raycast(UnityEngine.Ray, UnityEngine.RaycastHit ByRef, Single)`
- `UnityEngine.Vector3 ClosestPointOnBounds(UnityEngine.Vector3)`

**属性/字段：**
- `Boolean enabled`
- `UnityEngine.Rigidbody attachedRigidbody`
- `UnityEngine.ArticulationBody attachedArticulationBody`
- `Boolean isTrigger`
- `Single contactOffset`
- `UnityEngine.Bounds bounds`
- `Boolean hasModifiableContacts`
- `Boolean providesContacts`
- `Int32 layerOverridePriority`
- `UnityEngine.LayerMask excludeLayers`
- `UnityEngine.LayerMask includeLayers`
- `UnityEngine.PhysicMaterial sharedMaterial`
- `UnityEngine.PhysicMaterial material`

### Collider2D
- 暴露率: 98.31%
- 暴露成员: 58
- 完整名称: `Playables.Collider2D`

**方法：**
- `UnityEngine.Mesh CreateMesh(Boolean, Boolean)`
- `UInt32 GetShapeHash()`
- `Int32 GetShapes(UnityEngine.PhysicsShapeGroup2D)`
- `Int32 GetShapes(UnityEngine.PhysicsShapeGroup2D, Int32, Int32)`
- `Boolean IsTouching(UnityEngine.Collider2D)`
- `Boolean IsTouching(UnityEngine.Collider2D, UnityEngine.ContactFilter2D)`
- `Boolean IsTouching(UnityEngine.ContactFilter2D)`
- `Boolean IsTouchingLayers()`
- `Boolean IsTouchingLayers(Int32)`
- `Boolean OverlapPoint(UnityEngine.Vector2)`
- `UnityEngine.ColliderDistance2D Distance(UnityEngine.Collider2D)`
- `Int32 OverlapCollider(UnityEngine.ContactFilter2D, UnityEngine.Collider2D[])`
- ... 等 25 个方法

**属性/字段：**
- `Single density`
- `Boolean isTrigger`
- `Boolean usedByEffector`
- `Boolean usedByComposite`
- `UnityEngine.CompositeCollider2D composite`
- `UnityEngine.Vector2 offset`
- `UnityEngine.Rigidbody2D attachedRigidbody`
- `Int32 shapeCount`
- `UnityEngine.Bounds bounds`
- `UnityEngine.ColliderErrorState2D errorState`
- `UnityEngine.PhysicsMaterial2D sharedMaterial`
- `Int32 layerOverridePriority`
- `UnityEngine.LayerMask excludeLayers`
- `UnityEngine.LayerMask includeLayers`
- `UnityEngine.LayerMask forceSendLayers`
- ... 等 5 个属性

### Joint
- 暴露率: 93.75%
- 暴露成员: 15
- 完整名称: `Playables.Joint`

**属性/字段：**
- `UnityEngine.Rigidbody connectedBody`
- `UnityEngine.ArticulationBody connectedArticulationBody`
- `UnityEngine.Vector3 axis`
- `UnityEngine.Vector3 anchor`
- `UnityEngine.Vector3 connectedAnchor`
- `Boolean autoConfigureConnectedAnchor`
- `Single breakForce`
- `Single breakTorque`
- `Boolean enableCollision`
- `Boolean enablePreprocessing`
- `Single massScale`
- `Single connectedMassScale`
- `UnityEngine.Vector3 currentForce`
- `UnityEngine.Vector3 currentTorque`

### Physics
- 暴露率: 88.82%
- 暴露成员: 151
- 完整名称: `Playables.Physics`

**方法：**
- `<Static> Void IgnoreCollision(UnityEngine.Collider, UnityEngine.Collider, Boolean)`
- `<Static> Void IgnoreCollision(UnityEngine.Collider, UnityEngine.Collider)`
- `<Static> Boolean GetIgnoreLayerCollision(Int32, Int32)`
- `<Static> Boolean GetIgnoreCollision(UnityEngine.Collider, UnityEngine.Collider)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, Single, Int32, UnityEngine.QueryTriggerInteraction)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, Single, Int32)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, Single)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.RaycastHit ByRef, Single, Int32, UnityEngine.QueryTriggerInteraction)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.RaycastHit ByRef, Single, Int32)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.RaycastHit ByRef, Single)`
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.RaycastHit ByRef)`
- ... 等 131 个方法

**属性/字段：**
- `<Static> System.Int32 IgnoreRaycastLayer`
- `<Static> System.Int32 DefaultRaycastLayers`
- `<Static> System.Int32 AllLayers`
- `<Static> UnityEngine.Vector3 gravity`
- `<Static> Single bounceThreshold`
- `<Static> Single defaultMaxAngularSpeed`
- `<Static> UnityEngine.PhysicsScene defaultPhysicsScene`

### Physics2D
- 暴露率: 96.54%
- 暴露成员: 223
- 完整名称: `Playables.Physics2D`

**方法：**
- `<Static> Boolean Simulate(Single)`
- `<Static> Void SyncTransforms()`
- `<Static> Void IgnoreCollision(UnityEngine.Collider2D, UnityEngine.Collider2D)`
- `<Static> Void IgnoreCollision(UnityEngine.Collider2D, UnityEngine.Collider2D, Boolean)`
- `<Static> Boolean GetIgnoreCollision(UnityEngine.Collider2D, UnityEngine.Collider2D)`
- `<Static> Boolean GetIgnoreLayerCollision(Int32, Int32)`
- `<Static> Void SetLayerCollisionMask(Int32, Int32)`
- `<Static> Int32 GetLayerCollisionMask(Int32)`
- `<Static> Boolean IsTouching(UnityEngine.Collider2D, UnityEngine.Collider2D)`
- `<Static> Boolean IsTouching(UnityEngine.Collider2D, UnityEngine.Collider2D, UnityEngine.ContactFilter2D)`
- `<Static> Boolean IsTouching(UnityEngine.Collider2D, UnityEngine.ContactFilter2D)`
- `<Static> Boolean IsTouchingLayers(UnityEngine.Collider2D)`
- ... 等 189 个方法

**属性/字段：**
- `<Static> System.Int32 IgnoreRaycastLayer`
- `<Static> System.Int32 DefaultRaycastLayers`
- `<Static> System.Int32 AllLayers`
- `<Static> System.Int32 MaxPolygonShapeVertices`
- `<Static> UnityEngine.PhysicsScene2D defaultPhysicsScene`
- `<Static> Int32 velocityIterations`
- `<Static> Int32 positionIterations`
- `<Static> UnityEngine.Vector2 gravity`
- `<Static> Boolean queriesStartInColliders`
- `<Static> Boolean callbacksOnDisable`
- `<Static> Boolean reuseCollisionCallbacks`
- `<Static> Single velocityThreshold`
- `<Static> Single maxLinearCorrection`
- `<Static> Single maxAngularCorrection`
- `<Static> Single maxTranslationSpeed`
- ... 等 6 个属性

### RaycastHit
- 暴露率: 100.0%
- 暴露成员: 14
- 完整名称: `Playables.RaycastHit`

**属性/字段：**
- `UnityEngine.Collider collider`
- `Int32 colliderInstanceID`
- `UnityEngine.Vector3 point`
- `UnityEngine.Vector3 normal`
- `UnityEngine.Vector3 barycentricCoordinate`
- `Single distance`
- `Int32 triangleIndex`
- `UnityEngine.Vector2 textureCoord`
- `UnityEngine.Vector2 textureCoord2`
- `UnityEngine.Transform transform`
- `UnityEngine.Rigidbody rigidbody`
- `UnityEngine.ArticulationBody articulationBody`
- `UnityEngine.Vector2 lightmapCoord`

### RaycastHit2D
- 暴露率: 100.0%
- 暴露成员: 11
- 完整名称: `Playables.RaycastHit2D`

**方法：**
- `<Static> Boolean op_Implicit(UnityEngine.RaycastHit2D)`
- `Int32 CompareTo(UnityEngine.RaycastHit2D)`

**属性/字段：**
- `UnityEngine.Vector2 centroid`
- `UnityEngine.Vector2 point`
- `UnityEngine.Vector2 normal`
- `Single distance`
- `Single fraction`
- `UnityEngine.Collider2D collider`
- `UnityEngine.Rigidbody2D rigidbody`
- `UnityEngine.Transform transform`

## 渲染系统

### Material
- 暴露率: 81.94%
- 暴露成员: 127
- 完整名称: `Playables.Material`

**方法：**
- `Boolean HasProperty(Int32)`
- `Boolean HasProperty(System.String)`
- `Boolean HasFloat(System.String)`
- `Boolean HasFloat(Int32)`
- `Boolean HasInt(System.String)`
- `Boolean HasInt(Int32)`
- `Boolean HasInteger(System.String)`
- `Boolean HasInteger(Int32)`
- `Boolean HasTexture(System.String)`
- `Boolean HasTexture(Int32)`
- ... 等 104 个方法

**属性/字段：**
- `UnityEngine.Shader shader`
- `UnityEngine.Color color`
- `UnityEngine.Texture mainTexture`
- `UnityEngine.Vector2 mainTextureOffset`
- `UnityEngine.Vector2 mainTextureScale`
- `Int32 renderQueue`
- `UnityEngine.Rendering.LocalKeyword[] enabledKeywords`
- `UnityEngine.MaterialGlobalIlluminationFlags globalIlluminationFlags`
- `Boolean doubleSidedGI`
- `Boolean enableInstancing`
- `Int32 passCount`
- `System.String[] shaderKeywords`

### Renderer
- 暴露率: 95.56%
- 暴露成员: 43
- 完整名称: `Playables.Renderer`

**方法：**
- `Void ResetBounds()`
- `Void ResetLocalBounds()`
- `Boolean HasPropertyBlock()`
- `Void SetPropertyBlock(UnityEngine.MaterialPropertyBlock)`
- `Void SetPropertyBlock(UnityEngine.MaterialPropertyBlock, Int32)`
- `Void GetPropertyBlock(UnityEngine.MaterialPropertyBlock)`
- `Void GetPropertyBlock(UnityEngine.MaterialPropertyBlock, Int32)`
- `Void GetMaterials(System.Collections.Generic.List`1[UnityEngine.Material])`
- `Void SetSharedMaterials(System.Collections.Generic.List`1[UnityEngine.Material])`
- `Void SetMaterials(System.Collections.Generic.List`1[UnityEngine.Material])`
- ... 等 2 个方法

**属性/字段：**
- `UnityEngine.Bounds bounds`
- `UnityEngine.Bounds localBounds`
- `Boolean enabled`
- `Boolean isVisible`
- `UnityEngine.Rendering.ShadowCastingMode shadowCastingMode`
- `Boolean receiveShadows`
- `Boolean forceRenderingOff`
- `Boolean staticShadowCaster`
- `UnityEngine.MotionVectorGenerationMode motionVectorGenerationMode`
- `UnityEngine.Rendering.LightProbeUsage lightProbeUsage`
- `UnityEngine.Rendering.ReflectionProbeUsage reflectionProbeUsage`
- `UInt32 renderingLayerMask`
- ... 等 18 个属性

### Camera
- 暴露率: 85.0%
- 暴露成员: 119
- 完整名称: `Playables.Camera`

**方法：**
- `Void Reset()`
- `Void ResetTransparencySortSettings()`
- `Void ResetAspect()`
- `Void ResetCullingMatrix()`
- `Void SetReplacementShader(UnityEngine.Shader, System.String)`
- `Void ResetReplacementShader()`
- `Single GetGateFittedFieldOfView()`
- `UnityEngine.Vector2 GetGateFittedLensShift()`
- `Void SetTargetBuffers(UnityEngine.RenderBuffer, UnityEngine.RenderBuffer)`
- `Void SetTargetBuffers(UnityEngine.RenderBuffer[], UnityEngine.RenderBuffer)`
- ... 等 41 个方法

**属性/字段：**
- `<Static> System.Single kMinAperture`
- `<Static> System.Single kMaxAperture`
- `<Static> System.Int32 kMinBladeCount`
- `<Static> System.Int32 kMaxBladeCount`
- `Single nearClipPlane`
- `Single farClipPlane`
- `Single fieldOfView`
- `UnityEngine.RenderingPath renderingPath`
- `UnityEngine.RenderingPath actualRenderingPath`
- `Boolean allowHDR`
- `Boolean allowMSAA`
- `Boolean allowDynamicResolution`
- ... 等 55 个属性

### Mesh
- 暴露率: 78.6%
- 暴露成员: 169
- 完整名称: `Playables.Mesh`

**方法：**
- `Void SetIndexBufferParams(Int32, UnityEngine.Rendering.IndexFormat)`
- `UnityEngine.Rendering.VertexAttributeDescriptor GetVertexAttribute(Int32)`
- `Boolean HasVertexAttribute(UnityEngine.Rendering.VertexAttribute)`
- `Int32 GetVertexAttributeDimension(UnityEngine.Rendering.VertexAttribute)`
- `UnityEngine.Rendering.VertexAttributeFormat GetVertexAttributeFormat(UnityEngine.Rendering.VertexAttribute)`
- `Int32 GetVertexAttributeStream(UnityEngine.Rendering.VertexAttribute)`
- `Int32 GetVertexAttributeOffset(UnityEngine.Rendering.VertexAttribute)`
- `Int32 GetVertexBufferStride(Int32)`
- `Void ClearBlendShapes()`
- `System.String GetBlendShapeName(Int32)`
- ... 等 131 个方法

**属性/字段：**
- `UnityEngine.Rendering.IndexFormat indexFormat`
- `Int32 vertexBufferCount`
- `Int32 blendShapeCount`
- `Int32 bindposeCount`
- `UnityEngine.Matrix4x4[] bindposes`
- `Boolean isReadable`
- `Int32 vertexCount`
- `Int32 subMeshCount`
- `UnityEngine.Bounds bounds`
- `UnityEngine.Vector3[] vertices`
- `UnityEngine.Vector3[] normals`
- `UnityEngine.Vector4[] tangents`
- ... 等 14 个属性

### MeshFilter
- 暴露率: 75.0%
- 暴露成员: 3
- 完整名称: `Playables.MeshFilter`

**属性/字段：**
- `UnityEngine.Mesh sharedMesh`
- `UnityEngine.Mesh mesh`

### MeshRenderer
- 暴露率: 50.0%
- 暴露成员: 4
- 完整名称: `Playables.MeshRenderer`

**属性/字段：**
- `UnityEngine.Mesh additionalVertexStreams`
- `UnityEngine.Mesh enlightenVertexStream`
- `Int32 subMeshStartIndex`

### SkinnedMeshRenderer
- 暴露率: 75.0%
- 暴露成员: 12
- 完整名称: `Playables.SkinnedMeshRenderer`

**方法：**
- `Single GetBlendShapeWeight(Int32)`
- `Void SetBlendShapeWeight(Int32, Single)`
- `Void BakeMesh(UnityEngine.Mesh)`
- `Void BakeMesh(UnityEngine.Mesh, Boolean)`

**属性/字段：**
- `UnityEngine.SkinQuality quality`
- `Boolean updateWhenOffscreen`
- `Boolean forceMatrixRecalculationPerRender`
- `UnityEngine.Transform rootBone`
- `UnityEngine.Transform[] bones`
- `UnityEngine.Mesh sharedMesh`
- `Boolean skinnedMotionVectors`

### Light
- 暴露率: 62.5%
- 暴露成员: 30
- 完整名称: `Playables.Light`

**方法：**
- `Void Reset()`

**属性/字段：**
- `UnityEngine.LightType type`
- `Single spotAngle`
- `UnityEngine.Color color`
- `Single colorTemperature`
- `Boolean useColorTemperature`
- `Single intensity`
- `Single bounceIntensity`
- `Boolean useBoundingSphereOverride`
- `UnityEngine.Vector4 boundingSphereOverride`
- `Boolean useViewFrustumForShadowCasterCull`
- `Int32 shadowCustomResolution`
- `Single shadowBias`
- ... 等 16 个属性

### ParticleSystem
- 暴露率: 90.12%
- 暴露成员: 73
- 完整名称: `Playables.ParticleSystem`

**方法：**
- `Void SetParticles(Particle[], Int32, Int32)`
- `Void SetParticles(Particle[], Int32)`
- `Void SetParticles(Particle[])`
- `Int32 GetParticles(Particle[], Int32, Int32)`
- `Int32 GetParticles(Particle[], Int32)`
- `Int32 GetParticles(Particle[])`
- `Void SetCustomParticleData(System.Collections.Generic.List`1[UnityEngine.Vector4], UnityEngine.ParticleSystemCustomData)`
- `Int32 GetCustomParticleData(System.Collections.Generic.List`1[UnityEngine.Vector4], UnityEngine.ParticleSystemCustomData)`
- `PlaybackState GetPlaybackState()`
- `Void SetPlaybackState(PlaybackState)`
- ... 等 27 个方法

**属性/字段：**
- `Boolean isPlaying`
- `Boolean isEmitting`
- `Boolean isStopped`
- `Boolean isPaused`
- `Int32 particleCount`
- `Single time`
- `Single totalTime`
- `UInt32 randomSeed`
- `Boolean useAutoRandomSeed`
- `Boolean proceduralSimulationSupported`
- `Boolean has3DParticleRotations`
- `Boolean hasNonUniformParticleSizes`
- ... 等 23 个属性

### ParticleSystemRenderer
- 暴露率: 68.09%
- 暴露成员: 32
- 完整名称: `Playables.ParticleSystemRenderer`

**方法：**
- `Int32 GetMeshes(UnityEngine.Mesh[])`
- `Void SetMeshes(UnityEngine.Mesh[], Int32)`
- `Void SetMeshes(UnityEngine.Mesh[])`
- `Int32 GetMeshWeightings(Single[])`
- `Void SetMeshWeightings(Single[], Int32)`
- `Void SetMeshWeightings(Single[])`
- `Void SetActiveVertexStreams(System.Collections.Generic.List`1[UnityEngine.ParticleSystemVertexStream])`
- `Void GetActiveVertexStreams(System.Collections.Generic.List`1[UnityEngine.ParticleSystemVertexStream])`

**属性/字段：**
- `UnityEngine.ParticleSystemRenderSpace alignment`
- `UnityEngine.ParticleSystemRenderMode renderMode`
- `UnityEngine.ParticleSystemMeshDistribution meshDistribution`
- `UnityEngine.ParticleSystemSortMode sortMode`
- `Single lengthScale`
- `Single velocityScale`
- `Single cameraVelocityScale`
- `Single normalDirection`
- `Single shadowBias`
- `Single sortingFudge`
- `Single minParticleSize`
- `Single maxParticleSize`
- ... 等 11 个属性

## 动画系统

### Animator
- 暴露率: 95.3%
- 暴露成员: 142
- 完整名称: `Playables.Animator`

**方法：**
- `Single GetFloat(System.String)`
- `Single GetFloat(Int32)`
- `Void SetFloat(System.String, Single)`
- `Void SetFloat(System.String, Single, Single, Single)`
- `Void SetFloat(Int32, Single)`
- `Void SetFloat(Int32, Single, Single, Single)`
- `Boolean GetBool(System.String)`
- `Boolean GetBool(Int32)`
- `Void SetBool(System.String, Boolean)`
- `Void SetBool(Int32, Boolean)`
- `Int32 GetInteger(System.String)`
- `Int32 GetInteger(Int32)`
- ... 等 87 个方法

**属性/字段：**
- `Boolean isOptimizable`
- `Boolean isHuman`
- `Boolean hasRootMotion`
- `Single humanScale`
- `Boolean isInitialized`
- `UnityEngine.Vector3 deltaPosition`
- `UnityEngine.Quaternion deltaRotation`
- `UnityEngine.Vector3 velocity`
- `UnityEngine.Vector3 angularVelocity`
- `UnityEngine.Vector3 rootPosition`
- ... 等 32 个属性

### AnimationClip
- 暴露率: 78.95%
- 暴露成员: 15
- 完整名称: `Playables.AnimationClip`

**方法：**
- `Void SampleAnimation(UnityEngine.GameObject, Single)`
- `Void SetCurve(System.String, System.Type, System.String, UnityEngine.AnimationCurve)`
- `Void EnsureQuaternionContinuity()`
- `Void ClearCurves()`

**属性/字段：**
- `Single length`
- `Single frameRate`
- `UnityEngine.WrapMode wrapMode`
- `UnityEngine.Bounds localBounds`
- `Boolean humanMotion`
- `Boolean empty`
- `Boolean hasGenericRootTransform`
- `Boolean hasMotionFloatCurves`
- `Boolean hasMotionCurves`
- `Boolean hasRootCurves`

### AnimationCurve
- 暴露率: 100.0%
- 暴露成员: 22
- 完整名称: `Playables.AnimationCurve`

**方法：**
- `Single Evaluate(Single)`
- `Int32 AddKey(Single, Single)`
- `Int32 AddKey(UnityEngine.Keyframe)`
- `Int32 MoveKey(Int32, UnityEngine.Keyframe)`
- `Void ClearKeys()`
- `Void RemoveKey(Int32)`
- `Int32 GetHashCode()`
- `Void SmoothTangents(Int32, Single)`
- `<Static> UnityEngine.AnimationCurve Constant(Single, Single, Single)`
- `<Static> UnityEngine.AnimationCurve Linear(Single, Single, Single, Single)`
- `<Static> UnityEngine.AnimationCurve EaseInOut(Single, Single, Single, Single)`
- `Boolean Equals(System.Object)`
- ... 等 2 个方法

**属性/字段：**
- `UnityEngine.Keyframe[] keys`
- `UnityEngine.Keyframe Item [Int32]`
- `Int32 length`
- `UnityEngine.WrapMode preWrapMode`
- `UnityEngine.WrapMode postWrapMode`

### AnimatorControllerParameter
- 暴露率: 100.0%
- 暴露成员: 10
- 完整名称: `Playables.AnimatorControllerParameter`

**方法：**
- `Boolean Equals(System.Object)`
- `Int32 GetHashCode()`

**属性/字段：**
- `System.String name`
- `Int32 nameHash`
- `UnityEngine.AnimatorControllerParameterType type`
- `Single defaultFloat`
- `Int32 defaultInt`
- `Boolean defaultBool`

### AnimatorStateInfo
- 暴露率: 100.0%
- 暴露成员: 11
- 完整名称: `Playables.AnimatorStateInfo`

**方法：**
- `Boolean IsName(System.String)`
- `Boolean IsTag(System.String)`

**属性/字段：**
- `Int32 fullPathHash`
- `Int32 shortNameHash`
- `Single normalizedTime`
- `Single length`
- `Single speed`
- `Single speedMultiplier`
- `Int32 tagHash`
- `Boolean loop`

### AnimatorTransitionInfo
- 暴露率: 100.0%
- 暴露成员: 10
- 完整名称: `Playables.AnimatorTransitionInfo`

**方法：**
- `Boolean IsName(System.String)`
- `Boolean IsUserName(System.String)`

**属性/字段：**
- `Int32 fullPathHash`
- `Int32 nameHash`
- `Int32 userNameHash`
- `UnityEngine.DurationUnit durationUnit`
- `Single duration`
- `Single normalizedTime`
- `Boolean anyState`

## 音频系统

### AudioSource
- 暴露率: 77.59%
- 暴露成员: 45
- 完整名称: `Playables.AudioSource`

**方法：**
- `Void Play()`
- `Void Play(UInt64)`
- `Void PlayDelayed(Single)`
- `Void PlayScheduled(Double)`
- `Void PlayOneShot(UnityEngine.AudioClip)`
- `Void PlayOneShot(UnityEngine.AudioClip, Single)`
- `Void SetScheduledStartTime(Double)`
- `Void SetScheduledEndTime(Double)`
- `Void Stop()`
- `Void Pause()`
- ... 等 11 个方法

**属性/字段：**
- `Single volume`
- `Single pitch`
- `Single time`
- `Int32 timeSamples`
- `UnityEngine.AudioClip clip`
- `Boolean isPlaying`
- `Boolean isVirtual`
- `Boolean loop`
- `Boolean playOnAwake`
- `UnityEngine.AudioVelocityUpdateMode velocityUpdateMode`
- `Single panStereo`
- `Single spatialBlend`
- ... 等 11 个属性

### AudioClip
- 暴露率: 88.24%
- 暴露成员: 15
- 完整名称: `Playables.AudioClip`

**方法：**
- `Boolean LoadAudioData()`
- `Boolean UnloadAudioData()`
- `Boolean GetData(Single[], Int32)`
- `Boolean SetData(Single[], Int32)`
- `<Static> UnityEngine.AudioClip Create(System.String, Int32, Int32, Int32, Boolean)`

**属性/字段：**
- `Single length`
- `Int32 samples`
- `Int32 channels`
- `Int32 frequency`
- `UnityEngine.AudioClipLoadType loadType`
- `Boolean preloadAudioData`
- `Boolean ambisonic`
- `Boolean loadInBackground`
- `UnityEngine.AudioDataLoadState loadState`

## VRC 平台 API

### Networking
- 暴露率: 42.25%
- 暴露成员: 30
- 完整名称: `Platform.Networking`

**方法：**
- `<Static> Boolean IsOwner(VRC.SDKBase.VRCPlayerApi, UnityEngine.GameObject)`
- `<Static> Boolean IsOwner(UnityEngine.GameObject)`
- `<Static> VRC.SDKBase.VRCPlayerApi GetOwner(UnityEngine.GameObject)`
- `<Static> Void SetOwner(VRC.SDKBase.VRCPlayerApi, UnityEngine.GameObject)`
- `<Static> Boolean IsObjectReady(UnityEngine.GameObject)`
- `<Static> Void Destroy(UnityEngine.GameObject)`
- `<Static> System.String GetUniqueName(UnityEngine.GameObject)`
- `<Static> System.DateTime GetNetworkDateTime()`
- `<Static> Double GetServerTimeInSeconds()`
- `<Static> Int32 GetServerTimeInMilliseconds()`
- `<Static> Double CalculateServerDeltaTime(Double, Double)`
- `<Static> VRC.SDKBase.VRC_EventDispatcher GetEventDispatcher()`
- `<Static> Single SimulationTime(UnityEngine.GameObject)`
- `<Static> Single SimulationTime(VRC.SDKBase.VRCPlayerApi)`
- `<Static> Void RequestStorageUsageUpdate()`
- ... 等 6 个方法

**属性/字段：**
- `<Static> VRC.SDKBase.VRC_EventHandler SceneEventHandler`
- `<Static> Boolean IsNetworkSettled`
- `<Static> Boolean IsMaster`
- `<Static> Boolean IsClogged`
- `<Static> Boolean IsInstanceOwner`
- `<Static> VRC.SDKBase.VRCPlayerApi LocalPlayer`
- `<Static> VRC.SDKBase.VRCPlayerApi Master`
- `<Static> VRC.SDKBase.VRCPlayerApi InstanceOwner`

### VRCPlayerApi
- 暴露率: 43.2%
- 暴露成员: 89
- 完整名称: `Platform.VRCPlayerApi`

**方法：**
- `Boolean IsPlayerGrounded()`
- `VRC.SDKBase.VRCDroneApi GetDrone()`
- `<Static> VRC.SDKBase.VRCPlayerApi[] GetPlayers()`
- `<Static> VRC.SDKBase.VRCPlayerApi[] GetPlayers(VRC.SDKBase.VRCPlayerApi[])`
- `<Static> Int32 GetPlayerCount()`
- `<Static> Int32 GetPlayerId(VRC.SDKBase.VRCPlayerApi)`
- `<Static> VRC.SDKBase.VRCPlayerApi GetPlayerById(Int32)`
- `Boolean IsValid()`
- `Boolean IsOwner(UnityEngine.GameObject)`
- `TrackingData GetTrackingData(TrackingDataType)`
- `UnityEngine.Vector3 GetBonePosition(UnityEngine.HumanBodyBones)`
- `UnityEngine.Quaternion GetBoneRotation(UnityEngine.HumanBodyBones)`
- `VRC.SDKBase.VRC_Pickup GetPickupInHand(PickupHand)`
- `Void PlayHapticEventInHand(PickupHand, Single, Single, Single)`
- `Void TeleportTo(UnityEngine.Vector3, UnityEngine.Quaternion)`
- ... 等 66 个方法

**属性/字段：**
- `System.Boolean isLocal`
- `System.String displayName`
- `Boolean isMaster`
- `Boolean isInstanceOwner`
- `Boolean isSuspended`
- `Boolean isVRCPlus`
- `Int32 playerId`

### VRCShader
- 暴露率: 91.67%
- 暴露成员: 11
- 完整名称: `Platform.VRCShader`

**方法：**
- `<Static> Int32 PropertyToID(System.String)`
- `<Static> Void SetGlobalInteger(Int32, Int32)`
- `<Static> Void SetGlobalFloat(Int32, Single)`
- `<Static> Void SetGlobalTexture(Int32, UnityEngine.Texture)`
- `<Static> Void SetGlobalColor(Int32, UnityEngine.Color)`
- `<Static> Void SetGlobalVector(Int32, UnityEngine.Vector4)`
- `<Static> Void SetGlobalMatrix(Int32, UnityEngine.Matrix4x4)`
- `<Static> Void SetGlobalFloatArray(Int32, Single[])`
- `<Static> Void SetGlobalVectorArray(Int32, UnityEngine.Vector4[])`
- `<Static> Void SetGlobalMatrixArray(Int32, UnityEngine.Matrix4x4[])`

### VRCGraphics
- 暴露率: 100.0%
- 暴露成员: 17
- 完整名称: `Platform.VRCGraphics`

**方法：**
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture, UnityEngine.Material, Int32)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture, UnityEngine.Material)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture, UnityEngine.Vector2, UnityEngine.Vector2)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture, Int32, Int32)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.RenderTexture, UnityEngine.Vector2, UnityEngine.Vector2, Int32, Int32)`
- `<Static> Void Blit(UnityEngine.Texture, UnityEngine.Material, Int32, Int32)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[])`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock, UnityEngine.Rendering.ShadowCastingMode)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock, UnityEngine.Rendering.ShadowCastingMode, Boolean)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock, UnityEngine.Rendering.ShadowCastingMode, Boolean, Int32)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock, UnityEngine.Rendering.ShadowCastingMode, Boolean, Int32, UnityEngine.Camera)`
- `<Static> Void DrawMeshInstanced(UnityEngine.Mesh, Int32, UnityEngine.Material, UnityEngine.Matrix4x4[], Int32, UnityEngine.MaterialPropertyBlock, UnityEngine.Rendering.ShadowCastingMode, Boolean, Int32, UnityEngine.Camera, UnityEngine.Rendering.LightProbeUsage)`
- ... 等 1 个方法

### VRCUrl
- 暴露率: 61.54%
- 暴露成员: 8
- 完整名称: `Platform.VRCUrl`

**方法：**
- `<Static> Boolean IsNullOrEmpty(VRC.SDKBase.VRCUrl)`
- `System.String Get()`
- `System.String ToString()`
- `Boolean Equals(System.Object)`
- `Boolean Equals(VRC.SDKBase.VRCUrl)`
- `Int32 GetHashCode()`

**属性/字段：**
- `<Static> VRC.SDKBase.VRCUrl Empty`

### VRC_Pickup
- 暴露率: 66.67%
- 暴露成员: 22
- 完整名称: `Platform.VRC_Pickup`

**方法：**
- `Void Drop()`
- `Void Drop(VRC.SDKBase.VRCPlayerApi)`
- `Void GenerateHapticEvent(Single, Single, Single)`
- `Void PlayHaptics()`

**属性/字段：**
- `UnityEngine.ForceMode MomentumTransferMethod`
- `System.Boolean DisallowTheft`
- `UnityEngine.Transform ExactGun`
- `UnityEngine.Transform ExactGrip`
- `System.Boolean allowManipulationWhenEquipped`
- `VRC.SDKBase.VRC_Pickup+PickupOrientation orientation`
- `VRC.SDKBase.VRC_Pickup+AutoHoldMode AutoHold`
- `System.String InteractionText`
- `System.String UseText`
- `System.Single ThrowVelocityBoostMinSpeed`
- `System.Single ThrowVelocityBoostScale`
- `System.Boolean pickupable`
- `System.Single proximity`
- `VRC.SDKBase.VRCPlayerApi currentPlayer`
- `Boolean IsHeld`
- ... 等 2 个属性

### VRCStation
- 暴露率: 64.29%
- 暴露成员: 9
- 完整名称: `Platform.VRCStation`

**方法：**
- `Void UseStation(VRC.SDKBase.VRCPlayerApi)`
- `Void ExitStation(VRC.SDKBase.VRCPlayerApi)`

**属性/字段：**
- `VRC.SDKBase.VRCStation+Mobility PlayerMobility`
- `System.Boolean canUseStationFromStation`
- `UnityEngine.RuntimeAnimatorController animatorController`
- `System.Boolean disableStationExit`
- `System.Boolean seated`
- `UnityEngine.Transform stationEnterPlayerLocation`
- `UnityEngine.Transform stationExitPlayerLocation`

### VRC_AvatarPedestal
- 暴露率: 50.0%
- 暴露成员: 6
- 完整名称: `Platform.VRC_AvatarPedestal`

**方法：**
- `Void SwitchAvatar(System.String)`
- `Void SetAvatarUse(VRC.SDKBase.VRCPlayerApi)`

**属性/字段：**
- `System.String blueprintId`
- `UnityEngine.Transform Placement`
- `System.Boolean ChangeAvatarsOnUse`
- `System.Single scale`

## VRC 数据容器

### DataList
- 暴露率: 92.86%
- 暴露成员: 39
- 完整名称: `Data.DataList`

**方法：**
- `Void TrimExcess()`
- `Boolean SetValue(Int32, VRC.SDK3.Data.DataToken)`
- `Boolean TryGetValue(Int32, VRC.SDK3.Data.TokenType, VRC.SDK3.Data.DataToken ByRef)`
- `Boolean TryGetValue(Int32, VRC.SDK3.Data.DataToken ByRef)`
- `Void Insert(Int32, VRC.SDK3.Data.DataToken)`
- `Void InsertRange(Int32, VRC.SDK3.Data.DataList)`
- `VRC.SDK3.Data.DataList GetRange(Int32, Int32)`
- `VRC.SDK3.Data.DataList ShallowClone()`
- `VRC.SDK3.Data.DataList DeepClone()`
- `VRC.SDK3.Data.DataToken[] ToArray()`
- `Void Add(VRC.SDK3.Data.DataToken)`
- `Void AddRange(VRC.SDK3.Data.DataList)`
- `Boolean Contains(VRC.SDK3.Data.DataToken)`
- `Int32 IndexOf(VRC.SDK3.Data.DataToken)`
- `Int32 IndexOf(VRC.SDK3.Data.DataToken, Int32)`
- `Int32 IndexOf(VRC.SDK3.Data.DataToken, Int32, Int32)`
- `Int32 LastIndexOf(VRC.SDK3.Data.DataToken)`
- `Int32 LastIndexOf(VRC.SDK3.Data.DataToken, Int32)`
- `Int32 LastIndexOf(VRC.SDK3.Data.DataToken, Int32, Int32)`
- `Boolean Remove(VRC.SDK3.Data.DataToken)`
- ... 等 13 个方法

**属性/字段：**
- `Int32 Count`
- `Int32 Capacity`
- `VRC.SDK3.Data.DataToken Item [Int32]`

### DataDictionary
- 暴露率: 76.92%
- 暴露成员: 20
- 完整名称: `Data.DataDictionary`

**方法：**
- `Void SetValue(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.DataToken)`
- `Boolean TryGetValue(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.TokenType, VRC.SDK3.Data.DataToken ByRef)`
- `Boolean TryGetValue(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.DataToken ByRef)`
- `VRC.SDK3.Data.DataDictionary ShallowClone()`
- `VRC.SDK3.Data.DataDictionary DeepClone()`
- `Void Clear()`
- `Boolean Remove(VRC.SDK3.Data.DataToken)`
- `Boolean Remove(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.DataToken ByRef)`
- `Boolean ContainsKey(VRC.SDK3.Data.DataToken)`
- `Boolean ContainsValue(VRC.SDK3.Data.DataToken)`
- `VRC.SDK3.Data.DataList GetKeys()`
- `VRC.SDK3.Data.DataList GetValues()`
- `Void Add(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.DataToken)`
- `Boolean Equals(VRC.SDK3.Data.DataDictionary)`
- `Boolean Equals(System.Object)`
- `Int32 GetHashCode()`

**属性/字段：**
- `Int32 Count`
- `VRC.SDK3.Data.DataToken Item [VRC.SDK3.Data.DataToken]`

### DataToken
- 暴露率: 99.36%
- 暴露成员: 156
- 完整名称: `Data.DataToken`

**方法：**
- `<Static> Boolean op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> SByte op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Byte op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Int16 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> UInt16 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Int32 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> UInt32 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Int64 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> UInt64 op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Single op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> Double op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> System.String op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> VRC.SDK3.Data.DataDictionary op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> VRC.SDK3.Data.DataList op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> VRC.SDK3.Data.DataError op_Explicit(VRC.SDK3.Data.DataToken)`
- `<Static> VRC.SDK3.Data.DataToken op_Implicit(UnityEngine.Object)`
- `<Static> VRC.SDK3.Data.DataToken op_Implicit(Boolean)`
- `<Static> VRC.SDK3.Data.DataToken op_Implicit(SByte)`
- `<Static> VRC.SDK3.Data.DataToken op_Implicit(Byte)`
- `<Static> VRC.SDK3.Data.DataToken op_Implicit(Int16)`
- ... 等 95 个方法

**属性/字段：**
- `VRC.SDK3.Data.TokenType TokenType`
- `Boolean IsEmpty`
- `Boolean Boolean`
- `SByte SByte`
- `Byte Byte`
- `Int16 Short`
- `UInt16 UShort`
- `Int32 Int`
- `UInt32 UInt`
- `Int64 Long`
- ... 等 11 个属性

### VRCJson
- 暴露率: 100.0%
- 暴露成员: 3
- 完整名称: `Data.VRCJson`

**方法：**
- `<Static> Boolean TryDeserializeFromJson(System.String, VRC.SDK3.Data.DataToken ByRef)`
- `<Static> Boolean TrySerializeToJson(VRC.SDK3.Data.DataToken, VRC.SDK3.Data.JsonExportType, VRC.SDK3.Data.DataToken ByRef)`

## UnityEngine.UI

### Text
- 暴露率: 96.77%
- 暴露成员: 30
- 完整名称: `UI.Text`

**方法：**
- `Void FontTextureChanged()`
- `UnityEngine.TextGenerationSettings GetGenerationSettings(UnityEngine.Vector2)`
- `<Static> UnityEngine.Vector2 GetTextAnchorPivot(UnityEngine.TextAnchor)`
- `Void CalculateLayoutInputHorizontal()`
- `Void CalculateLayoutInputVertical()`

**属性/字段：**
- `UnityEngine.TextGenerator cachedTextGenerator`
- `UnityEngine.TextGenerator cachedTextGeneratorForLayout`
- `UnityEngine.Texture mainTexture`
- `UnityEngine.Font font`
- `System.String text`
- `Boolean supportRichText`
- `Boolean resizeTextForBestFit`
- `Int32 resizeTextMinSize`
- `Int32 resizeTextMaxSize`
- `UnityEngine.TextAnchor alignment`
- ... 等 14 个属性

### Image
- 暴露率: 96.88%
- 暴露成员: 31
- 完整名称: `UI.Image`

**方法：**
- `Void DisableSpriteOptimizations()`
- `Void OnBeforeSerialize()`
- `Void OnAfterDeserialize()`
- `Void SetNativeSize()`
- `Void CalculateLayoutInputHorizontal()`
- `Void CalculateLayoutInputVertical()`
- `Boolean IsRaycastLocationValid(UnityEngine.Vector2, UnityEngine.Camera)`

**属性/字段：**
- `UnityEngine.Sprite sprite`
- `UnityEngine.Sprite overrideSprite`
- `Type type`
- `Boolean preserveAspect`
- `Boolean fillCenter`
- `FillMethod fillMethod`
- `Single fillAmount`
- `Boolean fillClockwise`
- `Int32 fillOrigin`
- `Single alphaHitTestMinimumThreshold`
- ... 等 13 个属性

### Button
- 暴露率: 75.0%
- 暴露成员: 3
- 完整名称: `UI.Button`

**方法：**
- `Void OnPointerClick(UnityEngine.EventSystems.PointerEventData)`
- `Void OnSubmit(UnityEngine.EventSystems.BaseEventData)`

### Slider
- 暴露率: 95.65%
- 暴露成员: 22
- 完整名称: `UI.Slider`

**方法：**
- `Void SetValueWithoutNotify(Single)`
- `Void Rebuild(UnityEngine.UI.CanvasUpdate)`
- `Void LayoutComplete()`
- `Void GraphicUpdateComplete()`
- `Void OnPointerDown(UnityEngine.EventSystems.PointerEventData)`
- `Void OnDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnMove(UnityEngine.EventSystems.AxisEventData)`
- `UnityEngine.UI.Selectable FindSelectableOnLeft()`
- `UnityEngine.UI.Selectable FindSelectableOnRight()`
- `UnityEngine.UI.Selectable FindSelectableOnUp()`
- ... 等 3 个方法

**属性/字段：**
- `UnityEngine.RectTransform fillRect`
- `UnityEngine.RectTransform handleRect`
- `Direction direction`
- `Single minValue`
- `Single maxValue`
- `Boolean wholeNumbers`
- `Single value`
- `Single normalizedValue`

### ScrollRect
- 暴露率: 97.62%
- 暴露成员: 41
- 完整名称: `UI.ScrollRect`

**方法：**
- `Void Rebuild(UnityEngine.UI.CanvasUpdate)`
- `Void LayoutComplete()`
- `Void GraphicUpdateComplete()`
- `Boolean IsActive()`
- `Void StopMovement()`
- `Void OnScroll(UnityEngine.EventSystems.PointerEventData)`
- `Void OnInitializePotentialDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnBeginDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnEndDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnDrag(UnityEngine.EventSystems.PointerEventData)`
- ... 等 4 个方法

**属性/字段：**
- `UnityEngine.RectTransform content`
- `Boolean horizontal`
- `Boolean vertical`
- `MovementType movementType`
- `Single elasticity`
- `Boolean inertia`
- `Single decelerationRate`
- `Single scrollSensitivity`
- `UnityEngine.RectTransform viewport`
- `UnityEngine.UI.Scrollbar horizontalScrollbar`
- ... 等 16 个属性

### InputField
- 暴露率: 87.93%
- 暴露成员: 51
- 完整名称: `UI.InputField`

**方法：**
- `Void MoveTextEnd(Boolean)`
- `Void MoveTextStart(Boolean)`
- `Void OnBeginDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnEndDrag(UnityEngine.EventSystems.PointerEventData)`
- `Void OnPointerDown(UnityEngine.EventSystems.PointerEventData)`
- `Void ProcessEvent(UnityEngine.Event)`
- `Void OnUpdateSelected(UnityEngine.EventSystems.BaseEventData)`
- `Void ForceLabelUpdate()`
- `Void Rebuild(UnityEngine.UI.CanvasUpdate)`
- ... 等 10 个方法

**属性/字段：**
- `Boolean shouldHideMobileInput`
- `Boolean shouldActivateOnSelect`
- `System.String text`
- `Boolean isFocused`
- `Single caretBlinkRate`
- `Int32 caretWidth`
- `UnityEngine.UI.Text textComponent`
- `UnityEngine.UI.Graphic placeholder`
- `UnityEngine.Color caretColor`
- `Boolean customCaretColor`
- ... 等 20 个属性

### Selectable
- 暴露率: 100.0%
- 暴露成员: 27
- 完整名称: `UI.Selectable`

**方法：**
- `<Static> Int32 AllSelectablesNoAlloc(UnityEngine.UI.Selectable[])`
- `Boolean IsInteractable()`
- `UnityEngine.UI.Selectable FindSelectable(UnityEngine.Vector3)`
- `UnityEngine.UI.Selectable FindSelectableOnLeft()`
- `UnityEngine.UI.Selectable FindSelectableOnRight()`
- `UnityEngine.UI.Selectable FindSelectableOnUp()`
- `UnityEngine.UI.Selectable FindSelectableOnDown()`
- `Void OnMove(UnityEngine.EventSystems.AxisEventData)`
- `Void OnPointerDown(UnityEngine.EventSystems.PointerEventData)`
- `Void OnPointerUp(UnityEngine.EventSystems.PointerEventData)`
- ... 等 5 个方法

**属性/字段：**
- `<Static> UnityEngine.UI.Selectable[] allSelectablesArray`
- `<Static> Int32 allSelectableCount`
- `UnityEngine.UI.Navigation navigation`
- `Transition transition`
- `UnityEngine.UI.ColorBlock colors`
- `UnityEngine.UI.SpriteState spriteState`
- `UnityEngine.UI.AnimationTriggers animationTriggers`
- `UnityEngine.UI.Graphic targetGraphic`
- `Boolean interactable`
- `UnityEngine.UI.Image image`
- ... 等 1 个属性

## 约束系统

### ParentConstraint
- 暴露率: 100.0%
- 暴露成员: 21
- 完整名称: `Animations.ParentConstraint`

**方法：**
- `UnityEngine.Vector3 GetTranslationOffset(Int32)`
- `Void SetTranslationOffset(Int32, UnityEngine.Vector3)`
- `UnityEngine.Vector3 GetRotationOffset(Int32)`
- `Void SetRotationOffset(Int32, UnityEngine.Vector3)`
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `Boolean constraintActive`
- `Boolean locked`
- `Int32 sourceCount`
- `UnityEngine.Vector3 translationAtRest`
- `UnityEngine.Vector3 rotationAtRest`
- `UnityEngine.Vector3[] translationOffsets`
- `UnityEngine.Vector3[] rotationOffsets`
- ... 等 2 个属性

### PositionConstraint
- 暴露率: 100.0%
- 暴露成员: 14
- 完整名称: `Animations.PositionConstraint`

**方法：**
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `UnityEngine.Vector3 translationAtRest`
- `UnityEngine.Vector3 translationOffset`
- `UnityEngine.Animations.Axis translationAxis`
- `Boolean constraintActive`
- `Boolean locked`
- `Int32 sourceCount`

### RotationConstraint
- 暴露率: 100.0%
- 暴露成员: 14
- 完整名称: `Animations.RotationConstraint`

**方法：**
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `UnityEngine.Vector3 rotationAtRest`
- `UnityEngine.Vector3 rotationOffset`
- `UnityEngine.Animations.Axis rotationAxis`
- `Boolean constraintActive`
- `Boolean locked`
- `Int32 sourceCount`

### ScaleConstraint
- 暴露率: 100.0%
- 暴露成员: 14
- 完整名称: `Animations.ScaleConstraint`

**方法：**
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `UnityEngine.Vector3 scaleAtRest`
- `UnityEngine.Vector3 scaleOffset`
- `UnityEngine.Animations.Axis scalingAxis`
- `Boolean constraintActive`
- `Boolean locked`
- `Int32 sourceCount`

### LookAtConstraint
- 暴露率: 100.0%
- 暴露成员: 16
- 完整名称: `Animations.LookAtConstraint`

**方法：**
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `Single roll`
- `Boolean constraintActive`
- `Boolean locked`
- `UnityEngine.Vector3 rotationAtRest`
- `UnityEngine.Vector3 rotationOffset`
- `UnityEngine.Transform worldUpObject`
- `Boolean useUpObject`
- ... 等 1 个属性

### AimConstraint
- 暴露率: 100.0%
- 暴露成员: 19
- 完整名称: `Animations.AimConstraint`

**方法：**
- `Void GetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Void SetSources(System.Collections.Generic.List`1[UnityEngine.Animations.ConstraintSource])`
- `Int32 AddSource(UnityEngine.Animations.ConstraintSource)`
- `Void RemoveSource(Int32)`
- `UnityEngine.Animations.ConstraintSource GetSource(Int32)`
- `Void SetSource(Int32, UnityEngine.Animations.ConstraintSource)`

**属性/字段：**
- `Single weight`
- `Boolean constraintActive`
- `Boolean locked`
- `UnityEngine.Vector3 rotationAtRest`
- `UnityEngine.Vector3 rotationOffset`
- `UnityEngine.Animations.Axis rotationAxis`
- `UnityEngine.Vector3 aimVector`
- `UnityEngine.Vector3 upVector`
- ... 等 4 个属性

### ConstraintSource
- 暴露率: 100.0%
- 暴露成员: 3
- 完整名称: `Animations.ConstraintSource`

**属性/字段：**
- `UnityEngine.Transform sourceTransform`
- `Single weight`

## NavMesh 导航

### NavMesh
- 暴露率: 93.33%
- 暴露成员: 28
- 完整名称: `AI.NavMesh`

**方法：**
- `<Static> Boolean Raycast(UnityEngine.Vector3, UnityEngine.Vector3, UnityEngine.AI.NavMeshHit ByRef, Int32)`
- `<Static> Boolean CalculatePath(UnityEngine.Vector3, UnityEngine.Vector3, Int32, UnityEngine.AI.NavMeshPath)`
- `<Static> Boolean FindClosestEdge(UnityEngine.Vector3, UnityEngine.AI.NavMeshHit ByRef, Int32)`
- `<Static> Boolean SamplePosition(UnityEngine.Vector3, UnityEngine.AI.NavMeshHit ByRef, Single, Int32)`
- `<Static> Void SetAreaCost(Int32, Single)`
- `<Static> Single GetAreaCost(Int32)`
- `<Static> Int32 GetAreaFromName(System.String)`
- `<Static> UnityEngine.AI.NavMeshTriangulation CalculateTriangulation()`
- `<Static> UnityEngine.AI.NavMeshDataInstance AddNavMeshData(UnityEngine.AI.NavMeshData)`
- `<Static> UnityEngine.AI.NavMeshDataInstance AddNavMeshData(UnityEngine.AI.NavMeshData, UnityEngine.Vector3, UnityEngine.Quaternion)`
- `<Static> Void RemoveNavMeshData(UnityEngine.AI.NavMeshDataInstance)`
- `<Static> UnityEngine.AI.NavMeshLinkInstance AddLink(UnityEngine.AI.NavMeshLinkData)`
- `<Static> UnityEngine.AI.NavMeshLinkInstance AddLink(UnityEngine.AI.NavMeshLinkData, UnityEngine.Vector3, UnityEngine.Quaternion)`
- `<Static> Void RemoveLink(UnityEngine.AI.NavMeshLinkInstance)`
- `<Static> Boolean SamplePosition(UnityEngine.Vector3, UnityEngine.AI.NavMeshHit ByRef, Single, UnityEngine.AI.NavMeshQueryFilter)`
- ... 等 10 个方法

**属性/字段：**
- `<Static> System.Int32 AllAreas`
- `<Static> Single avoidancePredictionTime`

### NavMeshAgent
- 暴露率: 98.0%
- 暴露成员: 49
- 完整名称: `AI.NavMeshAgent`

**方法：**
- `Boolean SetDestination(UnityEngine.Vector3)`
- `Void ActivateCurrentOffMeshLink(Boolean)`
- `Void CompleteOffMeshLink()`
- `Boolean Warp(UnityEngine.Vector3)`
- `Void Move(UnityEngine.Vector3)`
- `Void ResetPath()`
- `Boolean SetPath(UnityEngine.AI.NavMeshPath)`
- `Boolean FindClosestEdge(UnityEngine.AI.NavMeshHit ByRef)`
- `Boolean Raycast(UnityEngine.Vector3, UnityEngine.AI.NavMeshHit ByRef)`
- `Boolean CalculatePath(UnityEngine.Vector3, UnityEngine.AI.NavMeshPath)`
- `Boolean SamplePathPosition(Int32, Single, UnityEngine.AI.NavMeshHit ByRef)`
- `Void SetAreaCost(Int32, Single)`
- `Single GetAreaCost(Int32)`

**属性/字段：**
- `UnityEngine.Vector3 destination`
- `Single stoppingDistance`
- `UnityEngine.Vector3 velocity`
- `UnityEngine.Vector3 nextPosition`
- `UnityEngine.Vector3 steeringTarget`
- `UnityEngine.Vector3 desiredVelocity`
- `Single remainingDistance`
- `Single baseOffset`
- `Boolean isOnOffMeshLink`
- `UnityEngine.AI.OffMeshLinkData currentOffMeshLinkData`
- `UnityEngine.AI.OffMeshLinkData nextOffMeshLinkData`
- `Boolean autoTraverseOffMeshLink`
- `Boolean autoBraking`
- `Boolean autoRepath`
- `Boolean hasPath`
- ... 等 20 个属性

### NavMeshSurface
- 暴露率: 95.83%
- 暴露成员: 23
- 完整名称: `Navigation.NavMeshSurface`

**方法：**
- `Void AddData()`
- `Void RemoveData()`
- `UnityEngine.AI.NavMeshBuildSettings GetBuildSettings()`
- `Void BuildNavMesh()`
- `UnityEngine.AsyncOperation UpdateNavMesh(UnityEngine.AI.NavMeshData)`

**属性/字段：**
- `Int32 agentTypeID`
- `Unity.AI.Navigation.CollectObjects collectObjects`
- `UnityEngine.Vector3 size`
- `UnityEngine.Vector3 center`
- `UnityEngine.LayerMask layerMask`
- `UnityEngine.AI.NavMeshCollectGeometry useGeometry`
- `Int32 defaultArea`
- `Boolean ignoreNavMeshAgent`
- `Boolean ignoreNavMeshObstacle`
- `Boolean overrideTileSize`
- `Int32 tileSize`
- `Boolean overrideVoxelSize`
- `Single voxelSize`
- `Single minRegionArea`
- `Boolean buildHeightMesh`
- ... 等 2 个属性

## UdonSharp 运行时

### IUdonEventReceiver
- 暴露率: 68.0%
- 暴露成员: 17
- 完整名称: `Interfaces.IUdonEventReceiver`

**方法：**
- `Void SendCustomEvent(System.String)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void RequestSerialization()`
- `Void SendCustomEventDelayedSeconds(System.String, Single, VRC.Udon.Common.Enums.EventTiming)`
- `Void SendCustomEventDelayedFrames(System.String, Int32, VRC.Udon.Common.Enums.EventTiming)`

**属性/字段：**
- `Boolean enabled`
- `Boolean DisableInteractive`
- `System.String InteractionText`

### NetworkCalling
- 暴露率: 100.0%
- 暴露成员: 14
- 完整名称: `UdonNetworkCalling.NetworkCalling`

**方法：**
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `<Static> Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.IUdonEventReceiver, VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `<Static> Int32 GetQueuedEvents(VRC.Udon.Common.Interfaces.IUdonEventReceiver, System.String)`
- `<Static> Int32 GetAllQueuedEvents()`

**属性/字段：**
- `<Static> Boolean InNetworkCall`
- `<Static> VRC.SDKBase.VRCPlayerApi CallingPlayer`

### UdonBehaviour
- 暴露率: 15.7%
- 暴露成员: 19
- 完整名称: `Enums.UdonBehaviour`

**方法：**
- `Void SendCustomEvent(System.String)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void SendCustomNetworkEvent(VRC.Udon.Common.Interfaces.NetworkEventTarget, System.String, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object, System.Object)`
- `Void RequestSerialization()`
- `Void SendCustomEventDelayedSeconds(System.String, Single, VRC.Udon.Common.Enums.EventTiming)`
- `Void SendCustomEventDelayedFrames(System.String, Int32, VRC.Udon.Common.Enums.EventTiming)`
- `System.Type GetProgramVariableType(System.String)`
- `Void SetProgramVariable(System.String, System.Object)`
- ... 等 1 个方法

**属性/字段：**
- `Boolean DisableInteractive`
- `System.String InteractionText`

## System 类型（常用）

### String
- 暴露率: 92.41%
- 暴露成员: 146
- 完整名称: `Diagnostics.String`

**方法：**
- `<Static> Int32 Compare(System.String, System.String)`
- `<Static> Int32 Compare(System.String, System.String, Boolean)`
- `<Static> Int32 Compare(System.String, System.String, System.StringComparison)`
- `<Static> Int32 Compare(System.String, System.String, System.Globalization.CultureInfo, System.Globalization.CompareOptions)`
- `<Static> Int32 Compare(System.String, System.String, Boolean, System.Globalization.CultureInfo)`
- `<Static> Int32 Compare(System.String, Int32, System.String, Int32, Int32)`
- `<Static> Int32 Compare(System.String, Int32, System.String, Int32, Int32, Boolean)`
- `<Static> Int32 Compare(System.String, Int32, System.String, Int32, Int32, Boolean, System.Globalization.CultureInfo)`
- `<Static> Int32 Compare(System.String, Int32, System.String, Int32, Int32, System.Globalization.CultureInfo, System.Globalization.CompareOptions)`
- `<Static> Int32 Compare(System.String, Int32, System.String, Int32, Int32, System.StringComparison)`
- `<Static> Int32 CompareOrdinal(System.String, System.String)`
- `<Static> Int32 CompareOrdinal(System.String, Int32, System.String, Int32, Int32)`
- `Int32 CompareTo(System.Object)`
- `Int32 CompareTo(System.String)`
- `Boolean EndsWith(System.String)`
- ... 等 125 个方法

**属性/字段：**
- `<Static> System.String Empty`
- `Int32 Length`

### Convert
- 暴露率: 96.52%
- 暴露成员: 305
- 完整名称: `Diagnostics.Convert`

**方法：**
- `<Static> Boolean ToBoolean(System.Object)`
- `<Static> Boolean ToBoolean(System.Object, System.IFormatProvider)`
- `<Static> Boolean ToBoolean(Boolean)`
- `<Static> Boolean ToBoolean(SByte)`
- `<Static> Boolean ToBoolean(Char)`
- `<Static> Boolean ToBoolean(Byte)`
- `<Static> Boolean ToBoolean(Int16)`
- `<Static> Boolean ToBoolean(UInt16)`
- `<Static> Boolean ToBoolean(Int32)`
- `<Static> Boolean ToBoolean(UInt32)`
- `<Static> Boolean ToBoolean(Int64)`
- `<Static> Boolean ToBoolean(UInt64)`
- `<Static> Boolean ToBoolean(System.String)`
- `<Static> Boolean ToBoolean(System.String, System.IFormatProvider)`
- `<Static> Boolean ToBoolean(Single)`
- ... 等 289 个方法

### Math
- 暴露率: 82.95%
- 暴露成员: 73
- 完整名称: `Diagnostics.Math`

**方法：**
- `<Static> Int16 Abs(Int16)`
- `<Static> Int32 Abs(Int32)`
- `<Static> Int64 Abs(Int64)`
- `<Static> SByte Abs(SByte)`
- `<Static> System.Decimal Abs(System.Decimal)`
- `<Static> Int64 BigMul(Int32, Int32)`
- `<Static> Int32 DivRem(Int32, Int32, Int32 ByRef)`
- `<Static> Int64 DivRem(Int64, Int64, Int64 ByRef)`
- `<Static> System.Decimal Ceiling(System.Decimal)`
- `<Static> System.Decimal Floor(System.Decimal)`
- `<Static> Double IEEERemainder(Double, Double)`
- `<Static> Double Log(Double, Double)`
- `<Static> Byte Max(Byte, Byte)`
- `<Static> System.Decimal Max(System.Decimal, System.Decimal)`
- `<Static> Double Max(Double, Double)`
- ... 等 55 个方法

**属性/字段：**
- `<Static> System.Double E`
- `<Static> System.Double PI`

### Type
- 暴露率: 46.59%
- 暴露成员: 82
- 完整名称: `Diagnostics.Type`

**方法：**
- `Boolean IsEnumDefined(System.Object)`
- `System.String GetEnumName(System.Object)`
- `System.String[] GetEnumNames()`
- `Boolean IsSubclassOf(System.Type)`
- `Boolean IsAssignableFrom(System.Type)`
- `System.Type GetType()`
- `System.Type GetElementType()`
- `Int32 GetArrayRank()`
- `System.Type GetGenericTypeDefinition()`
- `System.Type[] GetGenericArguments()`
- `System.Type[] GetGenericParameterConstraints()`
- `System.Type GetNestedType(System.String)`
- `<Static> System.Type[] GetTypeArray(System.Object[])`
- `Boolean IsInstanceOfType(System.Object)`
- `Boolean IsEquivalentTo(System.Type)`
- ... 等 15 个方法

**属性/字段：**
- `Boolean IsSerializable`
- `Boolean ContainsGenericParameters`
- `Boolean IsVisible`
- `System.String Namespace`
- `System.String FullName`
- `Boolean IsNested`
- `System.Type DeclaringType`
- `System.Type ReflectedType`
- `System.Type UnderlyingSystemType`
- `Boolean IsArray`
- ... 等 41 个属性

### Array
- 暴露率: 64.42%
- 暴露成员: 67
- 完整名称: `Diagnostics.Array`

**方法：**
- `<Static> System.Array CreateInstance(System.Type, Int64[])`
- `Void CopyTo(System.Array, Int32)`
- `System.Object Clone()`
- `<Static> Int32 BinarySearch(System.Array, System.Object)`
- `<Static> Void Copy(System.Array, System.Array, Int64)`
- `<Static> Void Copy(System.Array, Int64, System.Array, Int64, Int64)`
- `Void CopyTo(System.Array, Int64)`
- `Int64 GetLongLength(Int32)`
- `System.Object GetValue(Int64)`
- `System.Object GetValue(Int64, Int64)`
- `System.Object GetValue(Int64, Int64, Int64)`
- `System.Object GetValue(Int64[])`
- `<Static> Int32 BinarySearch(System.Array, Int32, Int32, System.Object)`
- `<Static> Int32 BinarySearch[T](T[], T)`
- `<Static> Int32 BinarySearch[T](T[], Int32, Int32, T)`
- ... 等 44 个方法

**属性/字段：**
- `Int64 LongLength`
- `Boolean IsFixedSize`
- `Boolean IsReadOnly`
- `Boolean IsSynchronized`
- `System.Object SyncRoot`
- `Int32 Length`
- `Int32 Rank`

### Regex
- 暴露率: 83.02%
- 暴露成员: 44
- 完整名称: `RegularExpressions.Regex`

**方法：**
- `<Static> Boolean IsMatch(System.String, System.String)`
- `<Static> Boolean IsMatch(System.String, System.String, System.Text.RegularExpressions.RegexOptions)`
- `<Static> Boolean IsMatch(System.String, System.String, System.Text.RegularExpressions.RegexOptions, System.TimeSpan)`
- `Boolean IsMatch(System.String)`
- `Boolean IsMatch(System.String, Int32)`
- `<Static> System.Text.RegularExpressions.Match Match(System.String, System.String)`
- `<Static> System.Text.RegularExpressions.Match Match(System.String, System.String, System.Text.RegularExpressions.RegexOptions)`
- `<Static> System.Text.RegularExpressions.Match Match(System.String, System.String, System.Text.RegularExpressions.RegexOptions, System.TimeSpan)`
- `System.Text.RegularExpressions.Match Match(System.String)`
- `System.Text.RegularExpressions.Match Match(System.String, Int32)`
- `System.Text.RegularExpressions.Match Match(System.String, Int32, Int32)`
- `<Static> System.Text.RegularExpressions.MatchCollection Matches(System.String, System.String)`
- `<Static> System.Text.RegularExpressions.MatchCollection Matches(System.String, System.String, System.Text.RegularExpressions.RegexOptions)`
- `<Static> System.Text.RegularExpressions.MatchCollection Matches(System.String, System.String, System.Text.RegularExpressions.RegexOptions, System.TimeSpan)`
- `System.Text.RegularExpressions.MatchCollection Matches(System.String)`
- ... 等 20 个方法

**属性/字段：**
- `<Static> System.TimeSpan InfiniteMatchTimeout`
- `<Static> Int32 CacheSize`
- `System.TimeSpan MatchTimeout`
- `System.Text.RegularExpressions.RegexOptions Options`
- `Boolean RightToLeft`

### StringBuilder
- 暴露率: 91.46%
- 暴露成员: 75
- 完整名称: `RegularExpressions.StringBuilder`

**方法：**
- `Int32 EnsureCapacity(Int32)`
- `System.String ToString()`
- `System.String ToString(Int32, Int32)`
- `System.Text.StringBuilder Clear()`
- `System.Text.StringBuilder Append(Char, Int32)`
- `System.Text.StringBuilder Append(Char[], Int32, Int32)`
- `System.Text.StringBuilder Append(System.String)`
- `System.Text.StringBuilder Append(System.String, Int32, Int32)`
- `System.Text.StringBuilder Append(System.Text.StringBuilder)`
- `System.Text.StringBuilder Append(System.Text.StringBuilder, Int32, Int32)`
- `System.Text.StringBuilder AppendLine()`
- `System.Text.StringBuilder AppendLine(System.String)`
- `Void CopyTo(Int32, Char[], Int32, Int32)`
- `System.Text.StringBuilder Insert(Int32, System.String, Int32)`
- `System.Text.StringBuilder Remove(Int32, Int32)`
- ... 等 49 个方法

**属性/字段：**
- `Int32 Capacity`
- `Int32 MaxCapacity`
- `Int32 Length`
- `Char Chars [Int32]`

---

## 相关知识

- `memory/api/udon-type-exposure.md` — Udon Type Exposure Tree 索引
- `memory/api/not-exposed.md` — 未暴露 API 黑名单
- `memory/rules/udonsharp-language-limits.md` — UdonSharp 语言限制
