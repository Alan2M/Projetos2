describe('Gestor - Excluir Entrevista', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve excluir uma entrevista da lista', () => {
    cy.visit('/gestor/entrevistas/?data=2025-06-20');
    cy.get('a.btn-danger').contains('Excluir').first().click();
    cy.contains('Entrevista excluída com sucesso!').should('exist');

  });
});