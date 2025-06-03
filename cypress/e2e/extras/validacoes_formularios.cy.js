describe('Validações de formulário', () => {
  it('não deve enviar o formulário de cadastro se campos obrigatórios estiverem vazios', () => {
    cy.visit('/cadastro/');
    cy.get('button[type="submit"]').click();
  });

  it('deve mostrar erro ao enviar senhas diferentes', () => {
    cy.visit('/cadastro/');
    cy.get('input[name="nome"]').type('Teste');
    cy.get('input[name="email"]').type('teste@teste.com');
    cy.get('input[name="cpf"]').type('123.456.789-00');
    cy.get('input[name="celular"]').type('(81) 91234-5678');
    cy.get('input[name="data-nascimento"]').type('2000-01-01');
    cy.get('select[name="curso"]').select(1);
    cy.get('input[name="senha"]').type('123456');
    cy.get('input[name="confirmar-senha"]').type('654321');
    cy.get('button[type="submit"]').click();
    cy.contains('senhas não coincidem').should('exist');
  });
});