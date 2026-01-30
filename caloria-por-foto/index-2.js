// Archivo: /api/meals.js

const userMeals = {}; // La misma base de datos simulada

export default function handler(req, res) {
    // Solo permitimos peticiones POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    const { userId, calories, protein, carbs, identifiedFoods } = req.body;

    if (!userId) {
        return res.status(400).json({ error: 'El ID del usuario (userId) es obligatorio.' });
    }

    const newMeal = {
        mealId: Date.now(),
        registeredAt: new Date().toISOString(),
        calories,
        protein,
        carbs,
        identifiedFoods,
    };

    if (!userMeals[userId]) {
        userMeals[userId] = [];
    }
    userMeals[userId].push(newMeal);

    console.log('Comida registrada en Vercel:', JSON.stringify(userMeals, null, 2));

    res.status(201).json({
        message: 'Comida registrada exitosamente.',
        savedMeal: newMeal,
    });
}
