Usage
=====


# Descriptive Analytics


### Params
* `tenant` 

### Notes
* All tanant chats

### Example
#### Request
```
/api/analytics/countchats/?tenant=1
```

#### Response
```
(0,)
```

### Params
* `tenant` 

### Notes
* All tanant chats in the last hour

### Example
#### Request
```
/api/analytics/cumulativehourlychats/?tenant=1
```

#### Response
```
[[{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}], [{'count': 0}]]
```

### Params
* `tenant` 

### Notes
* All tanant chats in the last hour

### Example
#### Request
```
/api/analytics/counthourlychats/?tenant=1
```

#### Response
```
(0,)
```

### Params
* `context` 

### Notes
* Countr all escalated issues in for a tenant

### Example
#### Request
```
/api/analytics/countescalatedissues
```

#### Response
```

```

### Params
* `context` 

### Notes
* Countr all escalated issues in the last one hour for a tenant
 

### Example
#### Request
```
/api/analytics/hourlycountescalatedissues
```

#### Response
```

```

### Params
* `context` 

### Notes
* Clients communication channels with their tenants

### Example
#### Request
```
/api/analytics/communicationchannels
```

#### Response
```

```

### Params
* `context` 

### Notes
* How frequent clients engage with tenants

### Example
#### Request
```
/api/analytics/engagementfrequency
```

#### Response
```

```

### Params
* `context` 

### Notes
* Hourly average response time during ineractions

### Example
#### Request
```
/api/analytics/hourlyaverageresponsetime
```

#### Response
```

```
### Params
* `context` 

### Notes
* All client satisfaction chats beetween a tenant and it's clients 

### Example
#### Request
```
/api/analytics/hourlyclientsatisfaction
```

#### Response
```

```

### Params
* `context` 

### Notes
* Least enanaged topics for a tenant

### Example
#### Request
```
/api/analytics/leasttopics
```

#### Response
```

```

### Params
* `context` 

### Notes
* Client satisfaction for a particular tenant

### Example
#### Request
```
/api/analytics/clientsatisfaction
```

#### Response
```

```

### Params
* `context` 

### Notes
* Most popular topics for a tenant

### Example
#### Request
```
/api/analytics/populartopics
```

#### Response
```

```

### Params
* `context` 

### Notes
* Average age of clients talking to a tenant


### Example
#### Request
```
/api/analytics/clientsaverageage
```

#### Response
```

```

### Params
* `context` 

### Notes
* City distribution of clients talking to a tenant


### Example
#### Request
```
/api/analytics/clientcitydistribution
```

#### Response
```

```

### Params
* `context` 

### Notes
* Country distribution of clients talking to a tenant

### Example
#### Request
```
/api/analytics/countrydistribution
```

#### Response
```

```

### Params
* `context` 

### Notes
* Gender distribution of clients talking to a tenant

### Example
#### Request
```
/api/analytics/genderdistribution
```

#### Response
```

```
### Params
* `context` 

### Notes
* State distribution of clients talking to a tenant

### Example
#### Request
```
/api/analytics/statedistribution
```

#### Response
```

```

### Params
* `context` 

### Notes
* Average number of comments per issue for a tenant

### Example
#### Request
```
/api/analytics/averagecomments
```

#### Response
```

```

### Params
* `context` 

### Notes
* How the community is growing

### Example
#### Request
```
/api/analytics/communitygrowthrate
```

#### Response
```

```

### Params
* `context` 

### Notes
* Total number of members belonging to a particular community in atea tenant

### Example
#### Request
```
/api/analytics/communitymembers
```

#### Response
```

```

### Params
* `context` 

### Notes
* Community rating based on users


### Example
#### Request
```
/api/analytics/communityrating
```

#### Response
```

```

### Params
* `context` 

### Notes
* Cumulative comments issue threads for all issues for tenant


### Example
#### Request
```
/api/analytics/cumulativecomments
```

#### Response
```

```

### Params
* `context` 

### Notes
* All issues related to a tenant

### Example
#### Request
```
/api/analytics/cumulativeissues
```

#### Response
```

```

### Params
* `context` 

### Notes
* Unique comments by clients on issues of a tenant

### Example
#### Request
```
/api/analytics/uniquecomments
```

#### Response
```

```

### Params
* `context` 

### Notes
* Total number of voice messages sent to all chat associated with a particular tenant

### Example
#### Request
```
/api/analytics/cumulativevoicemessage/?tenant=1
```

#### Response
```

```



### Params
* `context` 

### Notes
* Average number of voice messages sent in a chat

### Example
#### Request
```
/api/analytics/averagevoicemessageperchat/?tenant=1
```

#### Response
```

```

### Params
* `context` 

### Notes
* For a particular tenant return the issues assoiated with a particular clients

### Example
#### Request
```
/api/analytics/issueuserrelation
```

#### Response
```

```



### Params
* `context` 

### Notes
* For a particular tenant return the comments assoiated with a particular clients

### Example
#### Request
```
/api/analytics/commentsuserrelation
```

#### Response
```

```