describe('Mensagens de Sucesso e Erro', () => {
  it('deve exibir mensagem de erro no login inválido', () => {
    cy.visit('/login/');
    cy.get('input[name="email"]').type('usuario_teste@email.com');
    cy.get('input[name="senha"]').type('senhaerrada');
    cy.get('button[type="submit"]').click();
    cy.contains('E-mail ou senha incorretos!').should('exist');
  });

  it('deve exibir mensagem de sucesso após cadastro válido', () => {
    cy.visit('/cadastro/');
    const timestamp = Date.now();
    
    cy.get('input[name="nome"]').type('Usuário Repetido');
    cy.get('input[name="email"]').type(`user${timestamp}@teste.com`);    
    cy.get('input[name="cpf"]').type(`${timestamp.toString().slice(0, 3)}.${timestamp.toString().slice(3, 6)}.${timestamp.toString().slice(6, 9)}-00`);    
    cy.get('input[name="celular"]').type('(81) 91234-5678');
    cy.get('input[name="data-nascimento"]').type('2000-01-01');
    cy.get('select[name="curso"]').select('1');
    cy.get('input[name="senha"]').type('senha123');
    cy.get('input[name="confirmar-senha"]').type('senha123');
    cy.get('button[type="submit"]').click();
    cy.contains('Cadastro realizado com sucesso').should('exist');
  });
});