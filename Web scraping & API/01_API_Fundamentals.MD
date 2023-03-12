# API Fundamentals
This short document will introduce the idea of APIs (application programming interfaces). These are a fundamental building block of the cloud native approach (as we will see on the module) and really a fundamental component of modern software and the world we live in! Let's start with a useful video that explains the concept well:

https://user-images.githubusercontent.com/48418248/206932791-884abc1d-86f6-4b79-ba70-c0dd00e34417.mp4

The metaphor here (of the waiter in a restaurant) is a useful one I think for the uninitiated. Ultimately APIs are machine-to-machine middlemen that allow one application or service to speak to another. Often in user-focused settings, again as in the video, this is an application/service querying or writing to a an external datastore. This can be someone else's datastore (who understandably probably won't want to give you direct database access), but also could be within a single company ... i.e. different apps/services updating each other (a key component in the cloud native world).

Many (most?) APIs are built using [RESTful](https://restfulapi.net/) protocols. REST (standing for REpresentional State Transfer) is really a set of guidelines to standardise communications between these applications/services. Although we don't need to go through everything here its worth touching on some fundamentals. Some initial terminology of the key elements of an API interatcion:
- __The client__: The program that is connecting to the API. This is the app/service that is requesting information or requesting information be added.
- __The request__: What __the client__ is requesting from the API.   
- __The resource__: The information or object __the client__ is requesting. This could be flight availability (as in the video) or a photo from Facebook, or pretty much anything that may be served over the internet.
- __The server__: The place where __the resource__ lives (e.g. the database we want to query or update).
- __The response__: What __the server__ sends back over the API in response to __the request__ made by the __client__ (e.g. __the resource__).

REST APIs then communicate using [HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) as a protocol. HTTP allows four basic methods:
- __GET__ - to request a specific piece of information;
- __POST__ - to create a new resource;
- __PUT__ - to edit or update a resource;
- __DELETE__ - to (suprise, suprise) delete a resource.

For example, __the client__ may ask __the server__ to __GET__ the flight price of a given flight. After this __the client__ may request __the server__ to __POST__ a new customer booking record into their system (i.e. buy a flight ticket). We could also imagine future events such as updating the passenger name (a __PUT__ request) or cancelling the booking (a __DELETE__ request). Note these would all be seperate requests ... each request wil use only one HTTP method.

The actual client request may look something like this:

```http
GET https://api.fakesite.com/v1?id=1234
```

Here we are making a __GET__ request to the API URL querying for an item with the ID 1234. The full URL is known as the endpoint of the request.

The response we receive may look something like this:

```json
[
  {
    'status_code': 200,
    'id': 1234,
    'content': 'blah, blah, blah'
  }
]
```

The result includes the requested ID and the requested resource ("content"). We also get a "status_code" of 200 - which means "OK" (i.e. the request was succesful). Some other common codes are listed [here](https://restfulapi.net/http-status-codes/).

This gives a basic overview - although obviously there is much further we can (and will) go with this. In the next workbook we will actually make an API!
