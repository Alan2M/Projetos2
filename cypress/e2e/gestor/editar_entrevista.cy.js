describe('Gestor - Editar Entrevista', () => {
  beforeEach(() => {
    cy.loginGestor();
  });

  it('deve editar os dados de uma entrevista', () => {
    cy.visit('/gestor/entrevistas/?data=2025-06-02');
    cy.visit('/gestor/entrevistas/editar/4/');
    cy.get('input[name="data_hora"]').type('2025-06-20T11:00');
    cy.get('button[type="submit"]').click();
    cy.contains('Entrevista atualizada com sucesso').should('exist');
  });
});