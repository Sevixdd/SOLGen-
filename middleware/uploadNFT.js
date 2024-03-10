const fs = require('fs');
const { Connection, PublicKey, clusterApiUrl, Keypair } = require('@solana/web3.js');
const { Metaplex, keypairIdentity, toMetaplexFile, irysStorage } = require("@metaplex-foundation/js");
const { nftStorage } = require("@metaplex-foundation/js-plugin-nft-storage");

const { awsStorage } = require("@metaplex-foundation/js-plugin-aws");
const { S3Client } = require("@aws-sdk/client-s3");


//Alchemy: https://solana-devnet.g.alchemy.com/v2/XakZZ0VmAweRHhBV58UtkmzI1wdj5xNz

const awsClient = new S3Client({
    region: "eu-west-2",
    credentials: {
      accessKeyId: "AKIAQ3EGPPNKJDTSU4XI",
      secretAccessKey: "TIMmehP7IS6S1T9MTMNPu/3BjeZSBumNHX6YZDns",
    },
  });



// Load your Solana wallet
const secretKey = [
    9, 253, 191, 100, 222,  43, 204, 110, 239, 141,  31,
  184, 121,  61, 156,  93, 113, 111,  48, 242,  72, 203,
  107, 132,  32, 102, 243,  36,  62, 203,  83, 195, 239,
  192, 151,  89, 191, 142,  13, 216, 204, 236, 163, 132,
  198,  45,  97, 107, 111, 166,  75,  97, 222, 185, 175,
  156, 249,  89, 165, 159, 255,  57, 176,  56
]



const walletKeypair = Keypair.fromSecretKey(new Uint8Array(secretKey));

const alchemyUrl = 'https://devnet.helius-rpc.com/?api-key=29c133e7-03a3-4995-9ef2-86ec168c2e08'; //'';https://solana-devnet.g.alchemy.com/v2/XakZZ0VmAweRHhBV58UtkmzI1wdj5xNz
const connection = new Connection(alchemyUrl);

async function main() {
    // const metaplex = Metaplex.make(connection).use(keypairIdentity(walletKeypair)).use(irysStorage({address: 'https://devnet.irys.xyz',provideUrl: 'https://api.devnet.solana.com', timeout: 60000}));
    
    // const metaplex = Metaplex.make(connection).use(keypairIdentity(walletKeypair)).use(awsStorage(awsClient, 'nftstoragetoken'));


    const metaplex = Metaplex.make(connection).use(keypairIdentity(walletKeypair))
        .use(irysStorage({address: 'https://devnet.irys.xyz',provideUrl: 'https://api.devnet.solana.com', timeout: 60000}));



    // Assuming you have your audio file and metadata in the 'assets' directory
    const audioPath = '../backend2.0/assets/0.wav';
    const metadataPath = './assets/test.json';

    const audioBuffer = fs.readFileSync(audioPath);
    const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));

    const audioFile = toMetaplexFile(audioBuffer, audioPath);

    console.log('Uploading audio file...');
    console.log("audio file: ", audioFile)


    const response = await metaplex.storage().upload(audioFile);
    const uri = response;
    console.log('Audio file uploaded:', uri);


    // const { uri } = await metaplex.storage().upload(audioFile);
    metadata.animation_url = uri; // Update the metadata with the uploaded audio file URI

    console.log('Uploading metadata...');
    const re = await metaplex.nfts().uploadMetadata(metadata);

    const metadataUri = re.uri;

    console.log("metadataUri: ", metadataUri)



    console.log('Minting NFT...');
    const res = await metaplex.nfts().create({
        uri: metadataUri,
        name: metadata.name,
        sellerFeeBasisPoints: metadata.seller_fee_basis_points,
        // Additional properties as needed
    });
    const { nft } = res;

    console.log(`NFT minted successfully: ${JSON.stringify(nft)}`);

    // console.log(`NFT minted successfully: ${nft.mintAddress}`);
}

main().catch(console.error);
