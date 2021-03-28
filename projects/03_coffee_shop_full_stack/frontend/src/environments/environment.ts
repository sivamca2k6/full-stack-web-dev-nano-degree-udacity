
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'sivamca2k6.au.auth0.com', // the auth0 domain prefix
    audience: 'UdaCoffeAPI', // the audience set for the auth0 app
    clientId: 'Us6tybaYd4G6lBf45qnRwBatJatSsQHh', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
