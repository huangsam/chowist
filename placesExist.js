// Run `mongo chowist placesExist.js --quiet`

const placesExist = () => {
  let existFlag = false
  db.getCollectionNames().forEach((name) => {
    if (name == 'places') {
      existFlag = true
    }
  })
  return existFlag
}

let result = placesExist()
print(result)
