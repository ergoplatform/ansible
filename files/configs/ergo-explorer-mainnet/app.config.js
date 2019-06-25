var __APP_CONFIG__ = {
  apiUrl: 'https://api.ergoplatform.com',
  alternativeLogo: true, // true by default
  environments: [
     {
       name: 'Mainnet',
       url: 'https://explorer.ergoplatform.com',
     },
     {
       name: 'Testnet',
       url: 'https://testnet.ergoplatform.com',
     },
   ],
};

if (typeof global !== 'undefined') {
  global.__APP_CONFIG__ = __APP_CONFIG__;
}
