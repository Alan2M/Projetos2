describe('Aluno - Status da Inscrição', () => {
  beforeEach(() => {
    cy.visit('/login/');
    cy.get('input[name="email"]').type('novo@email.com');
    cy.get('input[name="senha"]').type('senha123');
    cy.get('select[name="tipo"]').select('aluno');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/');
  });

  it('deve acessar a página de status da inscrição', () => {
    cy.visit('/status');
    cy.contains('Status de Inscrição').should('exist');
  });

  it('deve mostrar mensagem adequada se inscrição ainda não foi feita', () => {
    cy.visit('/status');
    cy.contains('Você ainda não possui inscrição ativa.').should('exist');
  });
});
