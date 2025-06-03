describe('Gestor - Listar Alunos', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve mostrar a lista de alunos inscritos', () => {
    cy.visit('/gestor/alunos');
    cy.contains('Alunos Inscritos').should('exist');
    cy.get('table tbody tr').should('have.length.greaterThan', 0);
  });
});