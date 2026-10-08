# Security Requirements and Threat Model for json_search()

## 1. Context

The `json_search()` function is used to search data returned from a network infrastructure monitoring API.

The system has three main roles:

- **admin**: has the highest level of access.
- **operator**: can access operational network information.
- **viewer**: can view general monitoring information but should not access sensitive information.

The function must enforce role-based access control before returning sensitive fields.

## 2. Sensitive Assets

The JSON data may contain sensitive information such as:

- `apiKey`: authentication/API key information.
- `managementIpAddress`: management address used to identify or access network devices.
- `issueSummary`: monitoring information about network issues.

## 3. Access Control Policy

| Field | Admin | Operator | Viewer |
|---|---|---|---|
| `apiKey` | Allow | Deny | Deny |
| `managementIpAddress` | Allow | Allow | Deny |
| `issueSummary` | Allow | Allow | Allow |

## 4. Trust Boundary

The trust boundary exists between the user role requesting the data and the JSON data returned by the monitoring API.

If `json_search()` does not verify the user's role before returning search results, an unauthorized user may retrieve sensitive fields.

Therefore, role-based authorization must be enforced by `json_search()` before returning protected data.

## 5. Threat Model

### T01 - Information Disclosure

An unauthorized role, such as `viewer`, calls `json_search()` to search for `apiKey` or `managementIpAddress`.

If the function only searches for the requested key without checking the user's role, sensitive information may be disclosed.

**Impact:** Sensitive network infrastructure information or authentication information may be exposed.

**Mitigation:** `json_search()` must check the requested field against the access policy before returning results.

### T02 - Elevation of Privilege

A user with a lower-privileged role may attempt to access fields that are only available to higher-privileged roles.

For example, a `viewer` attempts to retrieve `apiKey`.

**Impact:** The user may obtain information beyond their authorized privilege level.

**Mitigation:** The function must enforce role-based access control for every search request, including recursive searches.

## 6. Security Requirements

### SR-01 - Role-based authorization

The system shall verify the caller's role before returning protected fields.

### SR-02 - API key protection

The system shall only return `apiKey` values to the `admin` role.

### SR-03 - Management IP protection

The system shall only return `managementIpAddress` values to `admin` and `operator` roles.

### SR-04 - Monitoring information access

The system may return `issueSummary` values to `admin`, `operator`, and `viewer` roles.

### SR-05 - Recursive authorization

Role-based access control shall remain enforced during recursive searches so that unauthorized users cannot obtain protected fields located inside nested dictionaries or lists.

## 7. Security Test Basis

The security requirements above shall be verified using security test cases.

Examples:

- `viewer` searches for `apiKey` → expected result: `[]`.
- `operator` searches for `apiKey` → expected result: `[]`.
- `admin` searches for `apiKey` → expected result: authorized results.
- `viewer` searches for `managementIpAddress` → expected result: `[]`.
- `operator` searches for `managementIpAddress` → expected result: authorized results.