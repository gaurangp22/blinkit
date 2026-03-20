import mongoose from "mongoose";
import dotenv from "dotenv";
import ProductModel from "./models/product.model.js";

dotenv.config();

const getImageForProduct = (productName = '') => {
  const nameToMatch = productName.toLowerCase();
  
  if (nameToMatch.includes('apple')) return 'https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('milk')) return 'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('bread')) return 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('egg')) return 'https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('banana')) return 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('onion')) return 'https://images.unsplash.com/photo-1618512496248-a07ce814d0fa?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('potato')) return 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('tomato')) return 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('cheese')) return 'https://images.unsplash.com/photo-1486297314227-2c9182ba83dc?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('butter')) return 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('chicken') || nameToMatch.includes('meat')) return 'https://images.unsplash.com/photo-1604503468506-a8da13d52723?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('fish') || nameToMatch.includes('salmon')) return 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('juice')) return 'https://images.unsplash.com/photo-1600271886742-f049cd451b02?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('water')) return 'https://images.unsplash.com/photo-1523362628745-0c64ce48eba2?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('chips') || nameToMatch.includes('snack')) return 'https://images.unsplash.com/photo-1566478989037-e924e50bbd1f?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('chocolate')) return 'https://images.unsplash.com/photo-1548907040-4baa42d10919?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('coffee')) return 'https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('tea')) return 'https://images.unsplash.com/photo-1576092762791-dd9e2220afa1?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('rice')) return 'https://images.unsplash.com/photo-1536304929831-ee1ca9d44906?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('oil')) return 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('soap') || nameToMatch.includes('wash')) return 'https://images.unsplash.com/photo-1600857062241-98e5dba7f214?auto=format&fit=crop&q=80&w=400';
  if (nameToMatch.includes('shampoo')) return 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&q=80&w=400';

  const seed = productName ? (productName.length + productName.charCodeAt(0)) % 10 : 1;
  const fallbacks = [
    'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1608686207856-001b95cf60ca?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1583258292688-d0213dc5a3a8?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1534723452862-4c874018d66d?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1506617564039-2f3b650b7010?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1590779033100-9f60a05a011d?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1608686207856-001b95cf60ca?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1543168256-4154204e3ab3?auto=format&fit=crop&q=80&w=400', 
    'https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&q=80&w=400'  
  ];
  return fallbacks[seed % fallbacks.length];
};

const seedDatabase = async () => {
    try {
        if(!process.env.MONGODB_URI) {
            console.error("MONGODB_URI not found in env variables!");
            process.exit(1);
        }
        await mongoose.connect(process.env.MONGODB_URI);
        console.log("Connected to DB...");

        const products = await ProductModel.find({});
        console.log(`Found ${products.length} products to update.`);

        let updatedCount = 0;
        for (const product of products) {
            const imageUrl = getImageForProduct(product.name);
            product.image = [imageUrl]; 
            await product.save();
            updatedCount++;
        }

        console.log(`Successfully updated ${updatedCount} products with real images.`);
        process.exit(0);
    } catch (error) {
        console.error("Error running script:", error);
        process.exit(1);
    }
}

seedDatabase();
