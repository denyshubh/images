import Chance from 'chance';

const chance = new Chance();

export default function generateFakeAnimals(numAnimals) {
  const animals = [];

  for (let i = 0; i < numAnimals; i++) {
    const animal = {
      id: Date.now() + i,
      genus: chance.word(),
      species: chance.word(),
      weight: chance.floating({ min: 1, max: 500, fixed: 2 }),
      location: {
        enclosureID: chance.guid(),
        cageID: chance.integer({ min: 1, max: 100 }),
      },
      age: chance.integer({ min: 1, max: 50 }),
      healthAssessment: chance.pickone(['Excellent', 'Good', 'Fair', 'Poor']),
      chronicDiseases: chance.bool({ likelihood: 30 })
        ? [chance.pickone(['Diabetes', 'Arthritis', 'Cancer', 'Heart disease'])]
        : [],
    };
    animals.push(animal);
  }

  return animals;
}
