import express from 'express';
import bodyParser from 'body-parser';
import generateFakeAnimals from './fakeAnimals.js';


const app = express();
app.use(bodyParser.json());

// Adding custom error handling middleware
app.use((err, req, res, next) => {
    res.status(err.status || 500);
    res.json({
        error: {
            message: err.message,
        },
    });
});

function validateAnimal(animal) {
    if (!animal.genus ||
        !animal.species ||
        !animal.weight ||
        !animal.location ||
        !animal.age ||
        !animal.healthAssessment) {
        return false;
    }

    return true;
}

const animals = generateFakeAnimals(30); // Generate 30 fake animals data

// Get a list of animals
app.get('/api/v1/animals', (req, res) => {
    res.set('Cache-Control', 'public, max-age=3600'); // Cache for 1 hour
    res.json(animals);
});


// Get an animal by ID
app.get('/api/v1/animals/:animal_id', (req, res) => {
    const animal = animals.find(a => a.id === parseInt(req.params.animal_id));
    if (!animal) {
        return res.status(404).json({
            error: 'Animal not found'
        });
    }
    res.json(animal);
});

// POST method to add a new animal
app.post('/api/v1/animals', (req, res, next) => {
    const newAnimal = req.body;

    if (!validateAnimal(newAnimal)) {
        const error = new Error('Invalid animal data');
        error.status = 400;
        return next(error);
    }

    animals.push(newAnimal);
    res.status(201).json(newAnimal);
});

// PUT method to update an existing animal
app.put('/api/v1/animals/:id', (req, res, next) => {
    const animalId = parseInt(req.params.id);
    const updatedAnimal = req.body;

    if (!validateAnimal(updatedAnimal)) {
        const error = new Error('Invalid animal data');
        error.status = 400;
        return next(error);
    }

    const animalIndex = animals.findIndex(animal => animal.id === animalId);
    // check if animal exists
    if (animalIndex === -1) {
        const error = new Error('Animal not found');
        error.status = 404;
        return next(error);
    }

    animals[animalIndex] = updatedAnimal;
    res.status(200).json(updatedAnimal);
});

// DELETE method to remove an animal
app.delete('/api/v1/animals/:id', (req, res, next) => {
    const animalId = parseInt(req.params.id);
    const animalIndex = animals.findIndex(animal => animal.id === animalId);
    // check if animal exists
    if (animalIndex === -1) {
        const error = new Error('Animal not found');
        error.status = 404;
        return next(error);
    }

    animals.splice(animalIndex, 1);
    res.status(204).end();
});


// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});