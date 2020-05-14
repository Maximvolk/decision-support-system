function checkGetRecommendationsResponseFirstTwo(first, second)  {
  return ({body, status}) => {
      expect(status).is.equal(200);
      expect(body, 'response array')
        .to.be.a('array')
        .to.have.lengthOf(5);
      body.every(i => expect(i).to.have.property('recommendation'));

      expect(body[0].recommendation === first).is.true;
      expect(body[1].recommendation === second).is.true;
  };
}

function checkGetRecommendationsResponse(resp)  {
  return ({body, status}) => {
    expect(status).is.equal(200);
    expect(body, 'response array')
      .to.be.a('array')
      .to.have.lengthOf(5);
    body.every(i => expect(i).to.have.property('recommendation'));

    expect(body.some(i => i.recommendation === resp)).is.true
  };
}

function checkAddingExistingRecommendation() {
    return ({body, status}) => {
      expect(status).is.equal(400);
      expect(body === 'Recommendation already exists').is.true
    };
}

function checkLeavingFeedbackOnNonexistentRecommendation() {
    return ({body, status}) => {
        expect(status).is.equal(400);
        expect(body === 'Specified recommendation does not exist').is.true;
    }
}

function checkLeavingFeedbackWithNonBooleanDidHelpParameter() {
    return ({body, status}) => {
        expect(status).is.equal(400);
        expect(body === 'Request is not valid, didHelp must be a boolean flag').is.true;
    }
}

it('GetRecommendations: permission denied', () => {
  cy.api(
    {
      url: '/DSS/GetRecommendations',
      body: {
        problemDescription: 'permission denied'
      },
      method: 'POST',
    }
  ).then(checkGetRecommendationsResponseFirstTwo(
      "Добавьте sudo в начало команды и попробуйте снова",
      "Отредактируйте права на файл/папку с помощью команды chmod. Проверить права можно командой ls -l"
  ))
});

it('GetRecommendations: not found', () => {
  cy.api(
    {
      url: '/DSS/GetRecommendations',
      body: {
        problemDescription: 'not found'
      },
      method: 'POST',
    }
  ).then(checkGetRecommendationsResponse("Проверьте правильность введенной команды"))
});

it('AddRecommendation: Проверьте правильность введенной команды', () => {
   cy.api(
       {
           url: '/DSS/AddRecommendation',
           body: {
               recommendation: 'Проверьте правильность введенной команды'
           },
           method: 'POST',
           failOnStatusCode: false,
       }
   ).then(checkAddingExistingRecommendation())
});

it('LeaveFeedback: nonexistent recommendation', () => {
    cy.api(
        {
            url: '/DSS/LeaveFeedback',
            body: {
                problemDescription: 'some problem',
                recommendation: 'nonexistent recommendation',
                didHelp: true
            },
            method: 'POST',
            failOnStatusCode: false,
        }
    ).then(checkLeavingFeedbackOnNonexistentRecommendation())
});

it('LeaveFeedback: send string (not bool) in didHelp field', () => {
    cy.api(
        {
            url: '/DSS/LeaveFeedback',
            body: {
                problemDescription: 'some problem',
                recommendation: 'nonexistent recommendation',
                didHelp: 'not bool'
            },
            method: 'POST',
            failOnStatusCode: false,
        }
    ).then(checkLeavingFeedbackWithNonBooleanDidHelpParameter())
});
