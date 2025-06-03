describe('Gestor - Calendário de Entrevistas', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve exibir o calendário com entrevistas marcadas', () => {
    cy.visit('/gestor/calendario');
    cy.get('table.calendar').should('exist');
  });
});