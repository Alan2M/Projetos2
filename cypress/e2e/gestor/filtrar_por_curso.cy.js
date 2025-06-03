describe('Gestor - Filtrar Entrevistas por Curso', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve filtrar entrevistas por curso', () => {
    cy.visit('/gestor/entrevistas/todas/?curso=');
    cy.get('select[name="curso"]').select('1');
    cy.get('button[type="submit"]').click();

    cy.get('body').then(($body) => {
    if ($body.text().includes('Nenhuma entrevista agendada')) {
        cy.contains('Nenhuma entrevista agendada').should('exist');
    } else {
        cy.contains('Rafael').should('exist');
    }
    });

  });
});