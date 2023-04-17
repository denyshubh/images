import express from 'express';
import bodyParser from 'body-parser';
import generateFakeAnimals from './fakeAnimals.js';


const app = express();
app.use(bodyParser.json());

const animals = generateFakeAnimals(30);

// Get a list of animals
app.get('/api/v1/animals', (req, res) => {
  res.json(animals);
});

// Add a new animal
app.post('/api/v1/animals', (req, res) => {
  const newAnimal = req.body;
  newAnimal.id = Date.now();
  animals.push(newAnimal);
  res.status(201).json({ id: newAnimal.id });
});

// Get an animal by ID
app.get('/api/v1/animals/:animal_id', (req, res) => {
  const animal = animals.find(a => a.id === parseInt(req.params.animal_id));
  if (!animal) {
    return res.status(404).json({ error: 'Animal not found' });
  }
  res.json(animal);
});

// Update an animal's information by ID
app.put('/api/v1/animals/:animal_id', (req, res) => {
  const animalIndex = animals.findIndex(a => a.id === parseInt(req.params.animal_id));
  if (animalIndex === -1) {
    return res.status(404).json({ error: 'Animal not found' });
  }
  animals[animalIndex] = { ...animals[animalIndex], ...req.body };
  res.json(animals[animalIndex]);
});

// Delete an animal by ID
app.delete('/api/v1/animals/:animal_id', (req, res) => {
  const animalIndex = animals.findIndex(a => a.id === parseInt(req.params.animal_id));
  if (animalIndex === -1) {
    return res.status(404).json({ error: 'Animal not found' });
  }
  animals.splice(animalIndex, 1);
  res.status(204).end();
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
